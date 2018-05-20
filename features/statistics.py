from .base import IFeaturesExtractor
from re import findall


class StatisticsFeaturesExtractor(IFeaturesExtractor):
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

    def extract_features(self, debate, speaker):
        numbers_count = 0
        per_count = 0
        phrases_count = 0

        for p in debate.enum_speaker_paragraphs(speaker):
            if not p.is_meta:
                numbers_count += len(findall(self.__NUMBERS_REGEX__, p.text))
                per_count += len(findall(self.__PERCENTAGES_REGEX__, p.text))
                t = p.text.lower()
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