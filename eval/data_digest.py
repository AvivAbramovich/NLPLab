from features.tokens import TokensListFeaturesExtractorBase
from nltk import word_tokenize
from numpy import array


class DataDigester:
    def __init__(self, *features_extractors):
        self.__extractors__ = features_extractors
        self.__data__ = []
        self.__labels__ = []

        self.__has_tokens_list_features_extractor = \
            any([isinstance(fe, TokensListFeaturesExtractorBase) for fe in self.__extractors__])

    def fit(self, debate):
        if self.__has_tokens_list_features_extractor:
            tokens_lists_lists_dict = {
                speaker:self.__create_tokens_lists_list(debate, speaker)
                for speaker in debate.speakers}

        for speaker in debate.speakers:
            features = []
            for extractor in self.__extractors__:
                if isinstance(extractor, TokensListFeaturesExtractorBase):
                    features += extractor._extract_features_from_tokens_(tokens_lists_lists_dict[speaker])
                else:
                    features += extractor.extract_features(debate, speaker)
            self.__data__.append(features)
            self.__labels__.append(int(speaker.stand_for))

    def digest(self):
        return array(self.__data__), array(self.__labels__)

    @staticmethod
    def __create_tokens_lists_list(debate, speaker):
        return [word_tokenize(p.text) for p in debate.enum_speaker_paragraphs(speaker, include_meta=False)]
