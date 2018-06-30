from abc import ABCMeta, abstractmethod


class ILabelingSystem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_label(self, debate_results):
        """
        :param debate_results: a common.results.DebateResults object
        :return: int. a label
        """
        pass