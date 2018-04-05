from schema.parse import parse_file
from sys import argv


if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')

    debate = parse_file(argv[1])
    print(debate)