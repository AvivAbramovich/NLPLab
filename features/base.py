from abc import ABCMeta, abstractmethod


class IFeaturesExtractor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features(self, speaker, paragraphs):
        """
        Extract features list
        :param speaker: Speaker object
        :param paragraphs: The speaker's paragraph from a certain debate
        :return: list of float represent the features extracted.
                Must returns the same number of features for each call and in the same order!
        """
        pass