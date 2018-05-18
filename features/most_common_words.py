from .base import IFeaturesExtractor
from nltk import word_tokenize


class MostCommonWordsFeatureExtractor(IFeaturesExtractor):
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

    def extract_features(self, speaker, paragraphs):
        features = [0]*len(self.words_sets)
        count = 0
        for paragraph in paragraphs:
            for token in word_tokenize(paragraph.text):
                # TODO: filter out PISUK
                count += 1
                flag = False
                for index, ws in enumerate(self.words_sets):
                    if flag or token in ws:
                        flag = True
                        features[index] += 1

        return [float(f) / count for f in features]



