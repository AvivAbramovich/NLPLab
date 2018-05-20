from features.tokens import TokensListFeaturesExtractorBase
from schema.parse import parse_file
from features.quotes_statistics import QuotesStatisticsFeaturesExtractor
from features.special_mark import MarksStatisticsFeaturesExtractor
from features.personal_words import PersonalWordsFeaturesExtractor

from sys import argv



if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')
    a = [4,2]
    b = [2,2]
    path = 'C:\\Users\\Lior\\Documents\\GitHub\\NLPLab\\outputs\\abolish-death-penalty.xml'
    debate = parse_file(path)
    for speaker in debate.speakers:
        print(PersonalWordsFeaturesExtractor().extract_features(debate,speaker))
    print(debate)