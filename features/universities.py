from .base import IFeaturesExtractor


class UniversitiesNamesFeaturesExtractor(IFeaturesExtractor):
    def __init__(self, words_list):
        """
        :param words_list: a list of the words
        """
        self.__words__ = words_list

    @staticmethod
    def from_file(path):
        with open(path) as fh:
            return UniversitiesNamesFeaturesExtractor(
                [line.strip().lower() for line in fh.readlines() if '#' not in line])

    def extract_features(self, debate, speaker):
        count = 0
        for paragraph in debate.enum_speaker_paragraphs(speaker):
            if not paragraph.is_meta:
                text = paragraph.text.lower()
                for word in self.__words__:
                    if word in text:
                        count += 1

        return [count]
