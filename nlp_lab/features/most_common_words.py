from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase
from io import open as io_open


class MostCommonWordsFeatureExtractor(ParagraphsFeaturesExtractorBase):
    def __init__(self, words_list, sizes):
        """
        :param words_list: a list of the words
        :param sizes: list of sizes, for example [1000, 50000].
                      The features would be number of words in each first x words for each x in the list + the whole list
                      total, len(sizes)+1 features
        """
        self.words_sets = []
        current_list = words_list
        for ind, size in enumerate(sizes):
            cur_size = size - (sizes[ind-1] if ind else 0)
            self.words_sets.append(current_list[:cur_size])
            current_list = current_list[cur_size:]

        if current_list:
            self.words_sets.append(current_list)

    @staticmethod
    def from_file(path, sizes):
        with io_open(path, encoding="utf-8") as fh:
            return MostCommonWordsFeatureExtractor(
                [line.strip().lower() for line in fh.readlines() if '#' not in line],
                sizes)

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        features = [0]*len(self.words_sets)
        count = 0
        for paragraph in paragraphs_list:
            for token in paragraph.as_tokens:
                _token = token.lower()
                if _token.isalpha():
                    count += 1
                    flag = False  # also contained in smaller list, so include in bigger lists
                    for index, ws in enumerate(self.words_sets):
                        if flag or _token in ws:
                            flag = True
                            features[index] += 1

        if count == 0:
            return [0] * len(features)
        return [float(f) / count for f in features]

    def features_descriptions(self):
        lens = [len(s) for s in self.words_sets]
        asums = [sum(lens[:i]) for i in range(1, len(lens)+1)]
        return ['per. of words from most common %d' % s for s in asums]