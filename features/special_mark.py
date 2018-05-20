from features.base import IFeaturesExtractor, abstractmethod, ABCMeta
from HelperStructure.ZipDebate import ZipDebate


class MarksStatisticsFeaturesExtractor(IFeaturesExtractor):
    __default_list__ = [
        '?',
        '!'
        # TODO: add more words!
    ]

    def __init__(self, special_marks=None):
        self.special_marks = special_marks if special_marks else self.__default_list__

    def extract_features(self, debate, speaker):

        zip_debate = ZipDebate(debate)
        list_sentences = []
        dict_special_mark = {key: [] for key in self.special_marks}
        feature_vector = []

        for zip_paragraph in zip_debate.enum_speaker_zip_paragraphs(speaker):
            for sentence in zip_paragraph.list_sentences:
                if sentence[-1] in self.special_marks:
                    dict_special_mark[sentence[-1]].append(sentence)
            list_sentences.extend(zip_paragraph.list_sentences)

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
