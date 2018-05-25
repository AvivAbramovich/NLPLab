from abc import ABCMeta, abstractmethod

from features.interfaces.base import IFeaturesExtractor


class ParagraphsFeaturesExtractorBase(IFeaturesExtractor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        """
        Extract features for list of paragraphs represents speaker (or multiple speakers)
        :param debate: a common.debate.Debate object
        :param paragraphs_list: list of common.paragraph.Paragraph objects
        :return: same as extract_features
        """
        pass

    def extract_features(self, debate, speaker):
        return self.extract_features_from_paragraphs(debate,
            self.split_to_paragraphs(debate, speaker))

    @staticmethod
    def split_to_paragraphs(debate, speaker):
        return [p for p in debate.enum_speaker_paragraphs(speaker)]