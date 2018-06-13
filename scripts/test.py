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

debate_scripts = [filename for filename in listdir('debates') if filename.endswith('.xml')]

for debate_filename in debate_scripts:
    print('extract features from "%s"' % debate_filename)
    debate = parse_file(join('debates', debate_filename))

    paragraphs_pro = [p for p in debate.transcript_paragraphs if p.speaker.stand_for == True]
    a = TalkToTheAudienceFeaturesExtractor().extract_features_from_paragraphs(debate, paragraphs_pro)
    paragraphs_a = [p for p in debate.transcript_paragraphs if p.speaker.stand_for == False]
    b = TalkToTheAudienceFeaturesExtractor().extract_features_from_paragraphs(debate,paragraphs_a)

    print(a)
    print(b)
