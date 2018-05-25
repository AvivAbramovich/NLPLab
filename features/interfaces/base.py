from abc import ABCMeta, abstractmethod


class IFeaturesExtractor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features(self, debate, speaker):
        """
        Extract features list
        :param debate: a Debate object
        :param speaker: Speaker object from the debate
        :return: list of float represent the features extracted.
                Must returns the same number of features for each call and in the same order!
        """
        pass

    @abstractmethod
    def features_descriptions(self):
        """
        :return: list that each element is a short str that describe the feature the extract features returns.
                    the list must be in the length of the result of extract_features
        """
        pass