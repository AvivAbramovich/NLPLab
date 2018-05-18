from .tokens import TokensListFeaturesExtractorBase


class MostCommonWordsFeatureExtractor(TokensListFeaturesExtractorBase):
    def __init__(self, words_list, sizes):
        """
        :param words_list: a list of the words
        :param sizes: list of sizes, for example [1000, 50000].
                      The features would be number of words in each first x words for each x in the list + the whole list
                      total, len(sizes)+1 features
        """
        self.words_sets = []
        current_list = words_list
        sum = 0
        for size in sizes:
            self.words_sets.append(current_list[:size-sum])
            current_list = current_list[size-sum:]
            sum += size

        if current_list:
            self.words_sets.append(current_list)

    @staticmethod
    def from_file(path, sizes):
        with open(path) as fh:
            return MostCommonWordsFeatureExtractor(
                [line.strip().lower() for line in fh.readlines() if '#' not in line],
                sizes)

    def _extract_features_from_tokens_(self, tokens_lists_generator):
        features = [0]*len(self.words_sets)
        count = 0
        for tokens_list in tokens_lists_generator:
            for token in tokens_list:
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



