from abc import ABCMeta, abstractmethod
from features.interfaces.base import IFeaturesExtractor
from nltk import sent_tokenize


class SentencesFeaturesExtractorBase(IFeaturesExtractor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features_from_sentences(self, sentences_list_list):
        """
        Extract features for list of paragraphs represents speaker (or multiple speakers)
        :param sentences_list_list: list of lists of str.
                    Each sub-list represents a paragraph, and each str in sentence in that paragraph
        :return: same as extract_features
        """
        pass

    def extract_features(self, debate, speaker):
        return self.extract_features_from_sentences(
            self.split_to_sentences(debate, speaker))

    @staticmethod
    def split_to_sentences(debate, speaker):
        return [sent_tokenize(p.text) for p in debate.enum_speaker_paragraphs(speaker)]