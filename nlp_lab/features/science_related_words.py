from nlp_lab.features.interfaces import ParagraphsFeaturesExtractorBase


class ScienceRelatedPhrasesFeaturesExtractor(ParagraphsFeaturesExtractorBase):
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

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        count = 0
        for paragraph in paragraphs_list:
            for token in paragraph.as_tokens:
                t = token.lower()
                for phrase in self.__phrases__:
                    if phrase in t:
                        count += 1

        return [count]

    def features_descriptions(self):
        return ['num. of science related phrases']



