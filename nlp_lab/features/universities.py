from nlp_lab.features.interfaces import ParagraphsFeaturesExtractorBase


class UniversitiesNamesFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def __init__(self, universities_names_list):
        """
        :param universities_names_list: a list of the words
        """
        self.__univ_names__ = universities_names_list

    @staticmethod
    def from_file(path):
        with open(path) as fh:
            return UniversitiesNamesFeaturesExtractor(
                [line.strip().lower() for line in fh.readlines() if '#' not in line])

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        count = 0
        for paragraph in paragraphs_list:
            for sentence in paragraph.as_sentences:
                text = sentence.lower()
                for univ_name in self.__univ_names__:
                    index = text.find(univ_name)
                    if index != -1:
                        # now, check that it's the actual name (and not "mit" inside "admit")
                        if index != 0 and text[index-1].isalpha():
                            continue
                        end_index = index + len(univ_name)
                        if len(text) != end_index and text[end_index].isalpha():
                            continue

                        count += 1

        return [count]

    def features_descriptions(self):
        return ['num. of universities names']