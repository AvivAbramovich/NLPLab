from features.tokens import TokensListFeaturesExtractorBase
from nltk import word_tokenize
from numpy import array
import csv


class DataDigester:
    def __init__(self, *features_extractors):
        """
        :param features_extractors: list of FeaturesExtractor objects
        """
        self.__extractors__ = features_extractors
        self.__data__ = []
        self.__labels__ = []

        self.__names__ = []
        self.__speakers_names__ = []

        self.__has_tokens_list_features_extractor = \
            any([isinstance(fe, TokensListFeaturesExtractorBase) for fe in self.__extractors__])

    def fit(self, debate, name=None):
        if self.__has_tokens_list_features_extractor:
            tokens_lists_lists_dict = {
                speaker:self.__create_tokens_lists_list(debate, speaker)
                for speaker in debate.speakers}

        for speaker in debate.speakers:
            features = []
            for extractor in self.__extractors__:
                if isinstance(extractor, TokensListFeaturesExtractorBase):
                    extractor_features = extractor._extract_features_from_tokens_(tokens_lists_lists_dict[speaker])
                else:
                    extractor_features = extractor.extract_features(debate, speaker)
                features += extractor_features

            if any([f != 0 for f in extractor_features]):
                self.__data__.append(features)
                self.__labels__.append(int(speaker.stand_for))
                self.__names__.append(name if name else '-')
                self.__speakers_names__.append(speaker.name)

    def digest(self):
        return array(self.__data__), array(self.__labels__)

    def export(self, path):
        with open(path, 'wb') as fh:
            wr = csv.writer(fh, quoting=csv.QUOTE_ALL)

            # headers
            headers = ['debate', 'speaker', 'label']
            for extractor in self.__extractors__:
                features_descs = extractor.features_descriptions()
                headers += features_descs
            wr.writerow(headers)
            del headers

            for ind in range(len(self.__names__)):
                row = [self.__names__[ind],
                       self.__speakers_names__[ind],
                       self.__labels__[ind]]
                row += self.__data__[ind]
                # row = [str(i).encode('utf-8') for i in row]

                try:
                    wr.writerow(row)
                except Exception as e:
                    print('Failed to write row %d to csv.\nError: %s\nRow: %s' % (ind, str(e), row))

    @staticmethod
    def __create_tokens_lists_list(debate, speaker):
        return [word_tokenize(p.text) for p in debate.enum_speaker_paragraphs(speaker, include_meta=False)]
