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


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('-p', help='path to input debate xml files')
    args_parser.add_argument('--csv', help='path to save the features as csv', default=None)
    args_parser.add_argument('-nz', action='store_true', help='don\'t zip the debates before extracting features')
    args_parser.add_argument('--labels', help='Labeling system. Options: "binary", "percentages", "bins"',
                             default='percentages')
    args_parser.add_argument('--bs', type=int, default=BinsChangeLabelsProvider.DEFAULT_BIN_SIZE,
                             help='Bins size. if using --labels bins, set the bin size. default=%d'
                                  % BinsChangeLabelsProvider.DEFAULT_BIN_SIZE)
    args_parser.add_argument('--online', action='store_true',
                             help='If using --labels [binary|bins], '
                                  'use this flag to base on online audience instead line audience')
    args_parser.add_argument('--pr', type=float, default=AverageLabelingSystem.DEFAULT_ONLINE_AUDIENCE_PROPORTION,
                             help='If using --label percentages, '
                                  'use this to set proportion of live audience in the average. '
                                  'Default=%.2f' % AverageLabelingSystem.DEFAULT_ONLINE_AUDIENCE_PROPORTION)
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

    labeling_system = None
    if args.labels == 'percentages':
        labeling_system = AverageLabelingSystem(PercentagesChangeLabelsProvider(), args.pr)
    elif args.labels == 'binary':
        labeling_system = PlainLabelingSystem(BinaryLabelProvider(), base_on_live_audience=not args.online)
    elif args.labels == 'bins':
        labeling_system = PlainLabelingSystem(BinsChangeLabelsProvider
                                              (PercentagesChangeLabelsProvider(), bin_size=args.bs),
                                              base_on_live_audience=not args.online)
    else:
        print('Unknown labeling system "%s"' % args.labels)
        exit(1)

    observer = TournamentDebatesObserver(features_extractors, labeling_system)

    debate_scripts = [filename for filename in listdir(args.p) if filename.endswith('.xml')]

    for debate_filename in debate_scripts:
        print('extract features from "%s"' % debate_filename)
        debate = parse_file(join(args.p, debate_filename))
        if not args.nz:
            debate = debate.zip()
        observer.observe(debate, name=debate_filename)

    data, labels = observer.digest()

    # classifiers
    classifiers = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]

    for cls in classifiers:
        scores = cross_val_score(cls, data, labels, cv=5)
        print('"%s" cross-validation average scores: %.3f' % (cls.__class__.__name__, sum(scores)/len(scores)))

    if args.csv:
        observer.export(args.csv)
