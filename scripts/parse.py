from schema.parse import parse_file
from nltk import sent_tokenize
from common import *
from sys import argv


def zip_debate(debate_from_xml):
    zipped_debate = Debate(debate_from_xml.speakers, [], debate_from_xml.debate_results)
    last_paragraph = Paragraph(None,'',None)
    new_paragraph = None
    paragraph: Paragraph
    for paragraph in debate_from_xml.transcript_paragraphs:
        if paragraph == last_paragraph:
            new_paragraph.text += paragraph.text
        else:
            if new_paragraph != None:
                new_paragraph.sentences = sent_tokenize(new_paragraph.text)
                zipped_debate.add_transcript_paragraph(new_paragraph)
            new_paragraph = Paragraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time, paragraph.is_meta)
            last_paragraph = Paragraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time, paragraph.is_meta)

    zipped_debate.add_transcript_paragraph(new_paragraph)

    return zipped_debate

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')

    debate = parse_file('C:\\Users\Lior\\PycharmProjects\\NLPLab-schema\\outputs\\abolish-death-penalty.xml')
    zip_debate = zip_debate(debate)

    print(debate)