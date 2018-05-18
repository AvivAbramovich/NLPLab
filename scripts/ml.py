from features import *
from eval.data_digest import DataDigester
from os.path import join
from os import listdir
from schema.parse import parse_file
from argparse import ArgumentParser
from math import ceil

# cross validation
from sklearn.model_selection import cross_val_score

# classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier



sizes = [1000, 10000, 50000]
test_rate = 0.1


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('-p', help='path to input debate xml files')
    args = args_parser.parse_args()

    digester = DataDigester(
        MostCommonWordsFeatureExtractor.from_file(join('resources', 'wiki-100k.txt'), sizes),
        WordsStatisticsFeaturesExtractor(),
        NotFunctionWordsFeaturesExtractor(),
        PowerfullWordsFeaturesExtractor())

    debate_scripts = [filename for filename in listdir(args.p) if filename.endswith('.xml')]

    for debate_filename in debate_scripts:
        print('extract features from "%s"' % debate_filename)
        debate = parse_file(join(args.p, debate_filename))
        digester.fit(debate)

    data, labels = digester.digest()

    # classifiers
    classifiers = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]

    for cls in classifiers:
        scores = cross_val_score(cls, data, labels, cv=5)
        print('"%s" cross-validation average scores: %.3f' % (cls.__class__.__name__, sum(scores)/len(scores)))