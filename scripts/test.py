from schema.parse import parse_file
from features.person_tagger import PersonStatisticsFeaturesExtractor
from sys import argv



if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')

    path = argv[1]
    debate = parse_file(path)
    for speaker in debate.speakers:
        print(PersonStatisticsFeaturesExtractor().extract_features(debate,speaker))
    print(debate)