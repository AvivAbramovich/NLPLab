from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase
from nltk import word_tokenize
import numpy as np


class SentencesStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        list_sentences = []

        for paragraph in paragraphs_list:
            list_sentences.extend(paragraph.as_sentences)

        if(list_sentences != []):
            array_len_sentences = np.array([len(word_tokenize(s)) for s in list_sentences])
        else:
            array_len_sentences = np.zeros(4)

        return [array_len_sentences.mean(),
                array_len_sentences.std(),
                array_len_sentences.max(),
                array_len_sentences.min()]

    def features_descriptions(self):
        return ['mean length of sentence',
                'std length of sentence'
                'max length of sentence',
                'min length of sentence']