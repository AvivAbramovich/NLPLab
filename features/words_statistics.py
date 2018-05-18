from .tokens import TokensListFeaturesExtractorBase
from nltk.corpus import stopwords as __stopwords__
from collections import defaultdict
from math import sqrt


class WordsStatisticsFeaturesExtractor(TokensListFeaturesExtractorBase):
    def __init__(self, stopwords=None):
        self.stopwords = stopwords if stopwords else __stopwords__.words('english')

    def _extract_features_from_tokens_(self, tokens_lists_generator):
        all_words_bag = defaultdict(int)
        no_sw_bag = defaultdict(int)

        for token_list in tokens_lists_generator:
            for token in token_list:
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
        if len(dictionary) == 0:
            return 0

        avg = sum(dictionary.values())/len(dictionary)
        std = 0
        for token, count in dictionary.items():
            std += (count - avg) ** 2

        return sqrt(std/len(dictionary))