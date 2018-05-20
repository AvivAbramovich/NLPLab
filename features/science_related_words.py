from .base import IFeaturesExtractor


class ScienceRelatedPhrasesFeaturesExtractor(IFeaturesExtractor):
    def __init__(self, phrases_list):
        """
        :param phrases_list: a list of the words
        """
        self.__phrases__ = phrases_list

    @staticmethod
    def from_file(path):
        with open(path) as fh:
            return ScienceRelatedPhrasesFeaturesExtractor(
                [line.strip().lower() for line in fh.readlines() if '#' not in line])

    def extract_features(self, debate, speaker):
        count = 0
        for paragraph in debate.enum_speaker_paragraphs(speaker):
            if not paragraph.is_meta:
                text = paragraph.text.lower()
                for word in self.__phrases__:
                    if word in text:
                        count += 1

        return [count]

    def features_descriptions(self):
        return ['num. of science related phrases']



