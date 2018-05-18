from abc import ABCMeta, abstractmethod


class IMachineLearningEvaluater:
    __metaclass__ = ABCMeta
    @abstractmethod
    def train(self, debate):
        pass

    @abstractmethod
    def test(self, debate):
        """
        :param debate:
        :return: bool (classified right)
        """
