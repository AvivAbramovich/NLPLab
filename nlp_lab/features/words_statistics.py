from collections import defaultdict
from math import sqrt
from nltk.corpus import stopwords as __stopwords__
from nlp_lab.features.interfaces import ParagraphsFeaturesExtractorBase


class WordsStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def __init__(self, stopwords=None):
        self.__stopwords__ = stopwords if stopwords else __stopwords__.words('english') # TODO: check if lower

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        all_words_bag = defaultdict(int)
        no_sw_bag = defaultdict(int)

        for paragraph in paragraphs_list:
            for token in paragraph.as_tokens:
                if token.isalpha():
                    _token = token.lower()
                    all_words_bag[_token] += 1
                    if _token not in self.__stopwords__:
                        no_sw_bag[_token] += 1

        return [len(all_words_bag),         # number of different tokens
                len(no_sw_bag),             # number of different tokens not include stopwords
                self.std(all_words_bag),    # std of different tokens
                self.std(no_sw_bag)]        # std of different tokens not include stopwords

    @staticmethod
    def std(dictionary):
        if len(dictionary) == 0:
            return 0

        avg = sum(dictionary.values())/len(dictionary)
        std = 0
        for token, count in dictionary.items():
            std += (count - avg) ** 2

        return sqrt(std/len(dictionary))

    def features_descriptions(self):
        return [
            'num. of different tokens',
            'num. of non-stopwords tokens',
            'std of tokens',
            'std of non-stopwords tokens'
        ]