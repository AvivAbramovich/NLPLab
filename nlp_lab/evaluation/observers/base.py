from abc import ABCMeta, abstractmethod


class IDebatesObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def observe(self, debate, name=None):
        pass

    @abstractmethod
    def digest(self):
        """
        Digest all the observed data and return data and labels
        :return: (Data, Labels) tuple where:
                    Data: numpy.ndarray with shape (x,y) represents the data
                    Labels: numpy.ndarray with shape (x,1) represents the labels,
                            where each label at row i corresponds to the i-th row in Data
        """
        pass

    @abstractmethod
    def export(self, file_path):
        """
        Export the data to csv
        :param file_path:
        """
        pass

    @abstractmethod
    def get_features_descriptions(self):
        """
        return list of each features description
        :param file_path:
        """
        pass
