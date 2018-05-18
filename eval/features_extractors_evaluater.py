from .base import IMachineLearningEvaluater


class FeaturesExtractorsEvaluater(IMachineLearningEvaluater):
    def __init__(self, sklearn_algorithm, *features_extractors):
        self.__extractors__ = features_extractors
        self.__algorithm__ = sklearn_algorithm

    def train(self, debate):
        data, labels = self.__read_debate__(debate)
        self.__algorithm__.fit(data, labels)

    def test(self, debate):
        data, labels = self.__read_debate__(debate)
        res = self.__algorithm__.predict(data)
        succeed = 0.0
        for i in range(len(labels)):
            if labels[i] == res[i]:
                succeed += 1
        return succeed / len(labels)

    def __read_debate__(self, debate):
        data = []
        labels = []
        for speaker in debate.speakers:
            features = []
            for features_extractor in self.__extractors__:
                features += features_extractor.extract_features(debate, speaker)
            data.append(features)
            labels.append(int(speaker.stand_for))

        return data, labels
