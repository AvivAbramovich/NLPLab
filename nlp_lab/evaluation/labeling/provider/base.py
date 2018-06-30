from abc import ABCMeta, abstractmethod


class ILabelProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def provide_label(self, results):
        """
        :param results: a common.results.Results object
        :return: a label (int)
        """
        pass