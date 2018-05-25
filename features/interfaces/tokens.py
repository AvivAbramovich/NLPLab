from nltk import word_tokenize
from features.interfaces.base import IFeaturesExtractor, abstractmethod, ABCMeta


class TokensListFeaturesExtractorBase(IFeaturesExtractor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features_from_tokens(self, tokens_lists_list):
        """
        :param tokens_lists_list: list of list of str, where each sub-list represents a paragraph,
                and each str is a in that paragraph token.
        :return: same as extract_features
        """
        pass

    def extract_features(self, debate, speaker):
        return self.extract_features_from_tokens(
            self.split_to_tokens(debate, speaker)
        )

    @staticmethod
    def split_to_tokens(debate, speaker):
        return [word_tokenize(p.text) for p in debate.enum_speaker_paragraphs(speaker)]