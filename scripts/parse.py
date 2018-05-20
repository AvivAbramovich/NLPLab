from schema.parse import parse_file
from sys import argv
from HelperStructure.ZipDebate import ZipDebate

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')
    path = 'C:\\Users\\Lior\\Documents\\GitHub\\NLPLab\\outputs\\abolish-death-penalty.xml'
    #path = argv[1]
    debate = parse_file(path)
    zipDebate = ZipDebate(debate)
    print(debate)