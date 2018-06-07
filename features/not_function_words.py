from nltk.corpus import stopwords as __stopwords__
from interfaces import ParagraphsFeaturesExtractorBase


class NotFunctionWordsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def __init__(self, words_to_ignore=None):
        self.__words__ = words_to_ignore if words_to_ignore else __stopwords__.words('english')

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        nf_count = 0
        total_count = 0

        for paragraph in paragraphs_list:
            for t in paragraph.as_tokens:
                token = t.lower()
                if token.isalpha():
                    total_count += 1
                    if token not in self.__words__:
                        nf_count += 1

        if total_count == 0:
            return [0]
        return [nf_count / float(total_count)]

    def features_descriptions(self):
        return ['per. of non function words']