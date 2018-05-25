from interfaces import SentencesFeaturesExtractorBase


class ScienceRelatedPhrasesFeaturesExtractor(SentencesFeaturesExtractorBase):
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

    def extract_features_from_sentences(self, _, sentences_list_list):
        count = 0
        for p in sentences_list_list:
            for sentence in p:
                text = sentence.lower()
                for word in self.__phrases__:
                    if word in text:
                        count += 1

        return [count]

    def features_descriptions(self):
        return ['num. of science related phrases']



