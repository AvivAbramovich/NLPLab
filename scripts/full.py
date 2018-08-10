from argparse import ArgumentParser
from os import listdir
from os.path import join
from time import time
import random
import numpy as np
# cross validation

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

# classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.metrics import accuracy_score


from nlp_lab.evaluation.observers.tournament import TournamentDebatesObserver
from nlp_lab.evaluation.observers.async_tournament import TournamentDebatesAsyncObserver
from nlp_lab.evaluation.labeling.provider import *
from nlp_lab.evaluation.labeling.system import *

from nlp_lab.features import *

from nlp_lab.schema.parse import parse_file

sizes = [1000, 10000, 50000]
k_best_sizes = [10, 20, 30, 50]
binary_indexes = [2, 3]


def test_on_classifiers(data, labels, cv=5, name=None, tabs=0):
    classifiers = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]


    if name:
        print(name + ':')
    print('Num classes: %d' % len(set(labels)))

    prefix = '\t' * tabs

    for cls in classifiers:
        print(prefix + cls.__class__.__name__)
        print(prefix + '\tTest on all features')
        scores = cross_val_score(cls, data, labels, cv=cv)
        print(prefix + '\t\tcross-validation average scores0 : %.3f\n' % (sum(scores) / len(scores)))

        for size in k_best_sizes:
            if size < data.shape[1]:
                print(prefix + '\tTest on %d best features' % size)
                new_data, selected_features = select_k_features(data, labels, size)
                scores = cross_val_score(cls, new_data, labels, cv=cv)
                print(prefix + '\t\tcross-validation average scores: %.3f' % (sum(scores) / len(scores)))
                #print(prefix + '\t\tthe indexes of the selected features are:')
                #print(prefix + '\t\t' + str(selected_features))
                print('')  # line separation between sizes


def test_on_debates(data,labels,cv = 5, name = None,tabs = 0):
    classifiers = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]

    if name:
        print(name + ':')

    num_debates = (int)(data.shape[0] / 5)
    print('Num classes: %d' % len(set(labels)))

    prefix = '\t' * tabs

    number_of_tests = int(num_debates * cv /100)
    for cls in classifiers:


        print(prefix + cls.__class__.__name__)
        tested_debates = random.sample(list(range(num_debates)), k = number_of_tests)
        test_indexes = []
        for a in tested_debates:
            test_indexes.extend(list(range(a*5,a*5+5)))

        train_feature = [data[x] for x in range(len(data)) if x not in test_indexes]
        tested_feature = [data[x] for x in range(len(data)) if x in test_indexes]
        train_labels = [labels[x] for x in range(len(labels)) if x not in test_indexes]
        tested_labels = [labels[x] for x in range(len(labels)) if x in test_indexes]

        score = 0
        for i in range(cv):
            cls.fit(train_feature, train_labels)
            predicted_vector = cls.predict(tested_feature)
            predicted_vector_real =[]
            for chunk_index in range(0,len(predicted_vector),5):
                chunk = predicted_vector[chunk_index: chunk_index + 5]
                median = np.median(chunk)
                predicted_vector_real.extend(np.repeat(median,5))

            score += accuracy_score(tested_labels,predicted_vector_real)
        score /= cv


        print(prefix + '\tTest on all features')
        print(prefix + '\t\tcross-validation average scores: %.3f' % score)
        print('')

        for size in k_best_sizes:
            if size < data.shape[1]:
                new_data, selected_features = select_k_features(data, labels, size)
                train_feature = [new_data[x] for x in range(len(new_data)) if x not in test_indexes]
                tested_feature = [new_data[x] for x in range(len(new_data)) if x in test_indexes]
                train_labels = [labels[x] for x in range(len(labels)) if x not in test_indexes]
                tested_labels = [labels[x] for x in range(len(labels)) if x in test_indexes]

                print(prefix + '\tTest on %d best features' % size)
               # print(prefix + '\t\tthe indexes of the selected features are:')
                #print(prefix + '\t\t' + str(selected_features))

                score = 0
                for i in range(cv):
                    cls.fit(train_feature, train_labels)
                    predicted_vector = cls.predict(tested_feature)
                    predicted_vector_real = []
                    for chunk_index in range(0, len(predicted_vector), 5):
                        chunk = predicted_vector[chunk_index: chunk_index + 5]
                        median = np.median(chunk)
                        predicted_vector_real.extend(np.repeat(median, 5))

                    score += accuracy_score(tested_labels, predicted_vector_real)
                score /= cv


                print(prefix + '\t\tcross-validation average scores: %.3f' % score)
                print('')


def select_k_features(data, labels, k):
    k_best = SelectKBest(score_func=chi2, k=k)
    new_features = k_best.fit_transform(data, labels)
    return new_features, [i for i, v in enumerate(k_best.get_support()) if v]


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('-p', help='path to input debate xml files')
    args_parser.add_argument('--cv', help='number of cross-validations folds. Default=5', default=5, type=int)
    args_parser.add_argument('--csv', help='path to save the features as csv', default=None)
    args_parser.add_argument('-nz', action='store_true', help='don\'t zip the debates before extracting features')
    args_parser.add_argument('--limit', help='take only the first N debates', type=int, default=None)
    args_parser.add_argument('--async', action='store_true', help='Process the debates async')
    args_parser.add_argument('--debug', action='store_true', help='Add debug printing')
    args = args_parser.parse_args()

    features_extractors = [
        MostCommonWordsFeatureExtractor.from_file(join('resources', 'wiki-100k.txt'), sizes),
        WordsStatisticsFeaturesExtractor(),
        NotFunctionWordsFeaturesExtractor(),
        PowerfulWordsFeaturesExtractor(),
        ScienceRelatedPhrasesFeaturesExtractor.from_file(join('resources', 'science.txt')),
        UniversitiesNamesFeaturesExtractor.from_file(join('resources', 'universities.txt')),
        StatisticsFeaturesExtractor(),
        AudienceReactionsFeaturesExtractor(),
        ParagraphsSpeakingTimeFeaturesExtractor(),
        PosStatisticsFeaturesExtractor(),
        PersonStatisticsFeaturesExtractor(),
        PersonalWordsFeaturesExtractor(),
        QuotesStatisticsFeaturesExtractor(),
        SentencesStatisticsFeaturesExtractor(),
        MarksStatisticsFeaturesExtractor(),
        TalkToTheAudienceFeaturesExtractor()
    ]

    main_labeling_system = AverageLabelingSystem(PercentagesChangeLabelsProvider())
    main_name = 'Average (80% live - 20% online)'
    alternative_ls = [
        (AverageLabelingSystem(PercentagesChangeLabelsProvider(), 0.5), 'Average (50%-50%'),
        (AverageLabelingSystem(PercentagesChangeLabelsProvider(), 0.8), 'Average (20% live - 80% online)'),
        (PlainLabelingSystem(BinaryLabelProvider()),'Binary on live audience'),
        (PlainLabelingSystem(BinaryLabelProvider(), base_on_live_audience=False),'Binary on online audience'),
        (PlainLabelingSystem(BinsChangeLabelsProvider
                             (PercentagesChangeLabelsProvider())),
         'Bins on live audience (bin size=%d)' % BinsChangeLabelsProvider.DEFAULT_BIN_SIZE),
        (PlainLabelingSystem(BinsChangeLabelsProvider
                             (PercentagesChangeLabelsProvider()),
                             base_on_live_audience=False),
         'Bins on online audience (bin size=%d)' % BinsChangeLabelsProvider.DEFAULT_BIN_SIZE),
        (PlainLabelingSystem(BinsChangeLabelsProvider
                             (PercentagesChangeLabelsProvider(), bin_size=35)),
         'Bins on live audience (bin size=%d)' % 35),
        (PlainLabelingSystem(BinsChangeLabelsProvider
                             (PercentagesChangeLabelsProvider(), bin_size=35),
                             base_on_live_audience=False),
         'Bins on online audience (bin size=%d)' % 35)
        ]

    observer_cls = TournamentDebatesAsyncObserver if args.async else TournamentDebatesObserver
    observer = observer_cls(features_extractors, main_labeling_system, [al[0] for al in alternative_ls], debug_print=args.debug)

    args.p = 'debates'
    debate_scripts = [filename for filename in listdir(args.p) if filename.endswith('.xml')]

    if args.limit:
        debate_scripts = debate_scripts[:args.limit]

    start = time()
    for debate_filename in debate_scripts:
        debate = parse_file(join(args.p, debate_filename)).as_ascii()

        if debate.is_empty:
            print('Debate "%s" has no transcript, skipping it' % debate_filename)
            continue

        if not args.nz:
            debate = debate.zip()

        print('extract features from "%s"' % debate_filename)
        if not observer.observe(debate, name=debate_filename):
            print('Failed to observe "%s"' % debate_filename)

    data, labels = observer.digest()
    alternative_labels = observer.get_alternative_labels()

    total_time = time() - start
    print('')
    print('Total features extraction time: %d seconds' % total_time)
    print('Total records: %d' % len(labels))

    if args.csv:
        observer.export(args.csv)

    print('Results base on %d debates:' % len(debate_scripts))

    print('arguments analysis:\n\n')
    test_on_classifiers(data, labels, args.cv, name=main_name, tabs=1)
    for ind in range(len(alternative_ls)):
        _labels = alternative_labels[:,ind]
        test_on_classifiers(data, _labels, args.cv, name=alternative_ls[ind][1], tabs=1)


    print('\n\n\n\n\n\n\n\n\ndebates analysis\n\n')
    for binary_ind in binary_indexes:
        _labels = alternative_labels[:, binary_ind]
        test_on_debates(data, _labels, args.cv, name=alternative_ls[binary_ind][1], tabs=1)

    '''
    print('\n\n\n\n\n\n\n\n\ndebates analysis: cv = 7\n\n')
    for binary_ind in binary_indexes:
        _labels = alternative_labels[:, binary_ind]
        test_on_debates(data, _labels, cv = 7, name=alternative_ls[binary_ind][1], tabs=1)



    print('\n\n\n\n\n\n\n\n\ndebates analysis: cv  = 3 \n\n')
    for binary_ind in binary_indexes:
        _labels = alternative_labels[:, binary_ind]
        test_on_debates(data, _labels, cv = 3, name=alternative_ls[binary_ind][1], tabs=1) '''

    print('Features extractors average time (per record):')
    time_stats = observer.get_average_extractor_time()
    # to list, order by time
    time_stats = list(time_stats.items())
    time_stats.sort(key=lambda t:t[1], reverse=True)
    for tup in time_stats:
        print('\t%s: %.4f seconds' % tup)

    print('Features descriptions:')
    for t in enumerate(observer.get_features_descriptions()):
        print('%d: %s' % t)

