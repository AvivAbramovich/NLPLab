from .base import IFeaturesExtractor
from nltk import word_tokenize
from nltk.corpus import stopwords as __stopwords__
from collections import defaultdict
from math import sqrt


class WordsStatisticsFeaturesExtractor(IFeaturesExtractor):
    def __init__(self, stopwords=None):
        self.stopwords = stopwords if stopwords else __stopwords__

    def extract_features(self, _, paragraphs):
        all_words_bag = defaultdict(int)
        no_sw_bag = defaultdict(int)

        for paragraph in paragraphs:
            for token in word_tokenize(paragraph.text):
                # TODO: filter out PISUK (',', '.', etc..)
                all_words_bag[token] += 1
                if token not in self.stopwords:
                    no_sw_bag[token] += 1

        return [len(all_words_bag),         # number of different tokens
                len(no_sw_bag),             # number of different tokens not include stopwords
                self.std(all_words_bag),    # std of different tokens
                self.std(no_sw_bag)]        # std of different tokens not include stopwords

    @staticmethod
    def std(dictionary):
        avg = sum(dictionary.values())/len(dictionary)
        std = 0
        for token, count in dictionary.items():
            std += (count - avg) ** 2

        return sqrt(std/len(dictionary))