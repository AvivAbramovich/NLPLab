from nltk import word_tokenize
from features.interfaces.base import IFeaturesExtractor, abstractmethod, ABCMeta


class TokensListFeaturesExtractorBase(IFeaturesExtractor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_features_from_tokens(self, debate, tokens_lists_list):
        """
        :param debate: a common.debate.Debate object
        :param tokens_lists_list: list of list of str, where each sub-list represents a paragraph,
                and each str is a in that paragraph token.
        :return: same as extract_features
        """
        pass

    def extract_features(self, debate, speaker):
        return self.extract_features_from_tokens(debate,
            self.split_to_tokens(debate, speaker)
        )

    @staticmethod
    def split_to_tokens(debate, speaker, ignore_meta=True):
        return [word_tokenize(p.text) for p in debate.enum_speaker_paragraphs(speaker)
                if not ignore_meta or not p.is_meta]