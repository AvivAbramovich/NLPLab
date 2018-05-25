from re import findall
from interfaces import SentencesFeaturesExtractorBase


class StatisticsFeaturesExtractor(SentencesFeaturesExtractorBase):
    __NUMBERS_REGEX__ = '\d+'
    __PERCENTAGES_REGEX__ = '\d+%'
    __phrases__ = [
        'grown',
        'decline',
        'in the last',
        'in the next',
        'exactly',
        'about to',
        # TODO: add more
    ]

    def extract_features_from_sentences(self, _, sentences_list_list):
        numbers_count = 0
        per_count = 0
        phrases_count = 0

        for p in sentences_list_list:
            for sentence in p:
                numbers_count += len(findall(self.__NUMBERS_REGEX__, sentence))
                per_count += len(findall(self.__PERCENTAGES_REGEX__, sentence))
                t = sentence.lower()
                for phrase in self.__phrases__:
                    if phrase in t:
                        phrases_count += 1

        return [numbers_count, per_count, phrases_count]

    def features_descriptions(self):
        return [
            'num. of numbers',
            'num. of percentages',
            'num. of statistics phrases'
        ]