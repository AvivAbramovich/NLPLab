from features.interfaces.base import IFeaturesExtractor
from features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase


class MarksStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __default_list__ = [
        '?',
        '!'
        # TODO: add more words!
    ]

    def __init__(self, special_marks=None):
        self.special_marks = special_marks if special_marks else self.__default_list__

    def extract_features_from_paragraphs(self, debate, paragraphs_list):

        list_sentences = []
        dict_special_mark = {key: [] for key in self.special_marks}
        feature_vector = []

        for paragraph in paragraphs_list:
            list_sentences.extend(paragraph.as_sentences)
            for sentence in paragraph.as_sentences:
                if sentence[-1] in self.special_marks:
                    dict_special_mark[sentence[-1]].append(sentence)

        len_special_mark = [len(dict_special_mark[key]) for key in dict_special_mark.keys()]
        sum_special_mark = [sum(len(s) for s in dict_special_mark[key]) for key in dict_special_mark.keys()]
        avg_special_mark = [0 if len_special_mark[i] == 0 else sum_special_mark[i] / len_special_mark[i] for i in
                            range(len(len_special_mark))]
        special_mark_ratio = [0 if len(list_sentences) == 0 else len_special_mark[i] / len(list_sentences) for i in
                              range(len(len_special_mark))]

        feature_vector.extend(len_special_mark)
        feature_vector.extend(sum_special_mark)
        feature_vector.extend(avg_special_mark)
        feature_vector.extend(special_mark_ratio)

        return feature_vector


    def features_descriptions(self):
        return [
                'num. of sentences with ?',
                'num. of sentences with !',
                'num. total sentences with ? len in words',
                'num. total sentences with ! len in words',
                'avg  sentences with ?  len',
                'avg  sentences with !  len',
                'percent of sentences with ?  to all sentences',
                'percent of sentences with !  to all sentences'
                ]