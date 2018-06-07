from argparse import ArgumentParser
from os import listdir
from os.path import join

# cross validation
from sklearn.model_selection import cross_val_score
# classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from evaluation.observers.tournament import TournamentDebatesObserver
from evaluation.labeling.provider import *
from evaluation.labeling.system import *

from features import *
from schema.parse import parse_file

sizes = [1000, 10000, 50000]


def test_on_classifiers(data, labels, cv=5):
    classifiers = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]

    for cls in classifiers:
        scores = cross_val_score(cls, data, labels, cv=cv)
        print('"%s" cross-validation average scores: %.3f' % (cls.__class__.__name__, sum(scores) / len(scores)))


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('-p', help='path to input debate xml files')
    args_parser.add_argument('--cv', help='number of cross-validations folds. Default=5', default=5, type=int)
    args_parser.add_argument('--csv', help='path to save the features as csv', default=None)
    args_parser.add_argument('-nz', action='store_true', help='don\'t zip the debates before extracting features')
    args = args_parser.parse_args()

    features_extractors = [
        MostCommonWordsFeatureExtractor.from_file(join('resources', 'wiki-100k.txt'), sizes),
        WordsStatisticsFeaturesExtractor(),
        NotFunctionWordsFeaturesExtractor(),
        PowerfulWordsFeaturesExtractor(),
        ScienceRelatedPhrasesFeaturesExtractor.from_file(join('resources', 'science.txt')),
        UniversitiesNamesFeaturesExtractor(join('resources', 'universities.txt')),
        StatisticsFeaturesExtractor(),
        AudienceReactionsFeaturesExtractor(),
        ParagraphsSpeakingTimeFeaturesExtractor()
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

    observer = TournamentDebatesObserver(features_extractors, main_labeling_system, [al[0] for al in alternative_ls])

    debate_scripts = [filename for filename in listdir(args.p) if filename.endswith('.xml')]

    for debate_filename in debate_scripts:
        print('extract features from "%s"' % debate_filename)
        debate = parse_file(join(args.p, debate_filename))
        if not args.nz:
            debate = debate.zip()
        observer.observe(debate, name=debate_filename)

    data, labels = observer.digest()
    alternative_labels = observer.get_alternative_labels()

    print('Results base on %d debates:' % len(debate_scripts))

    print(main_name + ':')
    test_on_classifiers(data, labels, args.cv)
    for ind in range(len(alternative_ls)):
        _labels = alternative_labels[:,ind]
        print(alternative_ls[ind][1] + ':')
        test_on_classifiers(data, _labels, args.cv)

    if args.csv:
        observer.export(args.csv)
