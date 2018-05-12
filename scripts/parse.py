import os

from common import *
from sys import argv
from schema.parse import parse_file
from nltk import sent_tokenize
from classifier.Classifier import ClassifierFactory
from Features.FeatureDebate import FeatureDebate

classifiers = ClassifierFactory()


def ZipDebate(debate_from_xml):
    zipped_debate = Debate(debate_from_xml.speakers, [], debate_from_xml.debate_results)
    last_paragraph = Paragraph(None,'',None)
    new_paragraph = None

    paragraph: Paragraph
    for paragraph in debate_from_xml.transcript_paragraphs:
        if paragraph == last_paragraph:
            if paragraph.is_meta:
                new_paragraph.crowed_reation.extend(paragraph.sentences)
            else:
                new_paragraph.text += paragraph.text

        else:
            if new_paragraph is not None:
                new_paragraph.sentences = sent_tokenize(new_paragraph.text)
                zipped_debate.add_transcript_paragraph(new_paragraph)
            new_paragraph = Paragraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time, paragraph.is_meta)
            last_paragraph = Paragraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time, paragraph.is_meta)

    zipped_debate.add_transcript_paragraph(new_paragraph)

    return zipped_debate


if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: parse <file path>')

    zip_debates = []
    features_debates = []
    path = 'C:\\Users\\Lior\\Documents\\GitHub\\NLPLab\\outputs'
    for debate_xml in os.listdir(path):
        try:
            print('running on:' + debate_xml)
            debate = parse_file(path + '\\' + debate_xml)
            zip_debate = ZipDebate(debate)
            zip_debates.append(zip_debate)
            features_debates.append(FeatureDebate(zip_debate))
        except Exception as e:
            print(debate_xml)

    print(debate)