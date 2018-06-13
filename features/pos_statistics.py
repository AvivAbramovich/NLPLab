from features.interfaces import ParagraphsFeaturesExtractorBase
from nltk import pos_tag,word_tokenize


class PosStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __default_list__ = [
        'JJ',
        'JJR',
        'RB'
        # TODO: add more words!
    ]

    def __init__(self, words=None):
        self.__pos__ = words if words else self.__default_list__

    def extract_features_from_paragraphs(self, debate, paragraphs_list):

        total_token = 0
        dict_special_mark = {key: 0 for key in self.__pos__}
        feature_vector = []

        for paragraph in paragraphs_list:
            for sentence in paragraph.as_sentences:
                pos_tagger = pos_tag(word_tokenize(sentence))
                for token in pos_tagger:
                    total_token += 1
                    if token[1] in self.__pos__:
                        dict_special_mark[token[1]] += 1

        len_special_mark = [dict_special_mark[key] for key in dict_special_mark.keys()]
        special_mark_ratio = [0 if total_token == 0 else len_special_mark[i] / total_token for i in range(len(len_special_mark))]

        feature_vector.extend(len_special_mark)
        feature_vector.extend(special_mark_ratio)

        return feature_vector

    def features_descriptions(self):
            return [
                'num. of ADJ',
                'num. of Adjective, comparative',
                'num. of Adverb',
                'percent of sentences with ADJ  to all sentences',
                'percent of sentences with Adjective, comparative  to all sentences',
                'percent of sentences with Adverb  to all sentences',
            ]

