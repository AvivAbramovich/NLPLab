from features.base import IFeaturesExtractor, abstractmethod, ABCMeta
from nltk import word_tokenize


class TokensListFeaturesExtractorBase(IFeaturesExtractor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _extract_features_from_tokens_(self, tokens_lists_generator):
        """
        :param tokens_lists_generator: generator of list of tokens (each item is paragraph, and the list is the paragraph's tokens)
        :return: same as extract_features
        """

    def extract_features(self, debate, speaker):
        return self._extract_features_from_tokens_(
            self.__tokens_generator__(debate, speaker)
        )

    @staticmethod
    def __tokens_generator__(debate, speaker):
        for p in debate.enum_speaker_paragraphs(speaker):
            yield word_tokenize(p.text)