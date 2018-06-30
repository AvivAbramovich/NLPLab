from nlp_lab.features.interfaces import ParagraphsFeaturesExtractorBase


class UniversitiesNamesFeaturesExtractor(ParagraphsFeaturesExtractorBase):
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

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        count = 0
        for paragraph in paragraphs_list:
            for sentence in paragraph.as_tokens:
                text = sentence.lower()
                for word in self.__words__:
                    if word in text:
                        count += 1

        return [count]

    def features_descriptions(self):
        return ['num. of universities names']