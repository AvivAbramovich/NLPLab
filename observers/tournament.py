from base import IDebatesObserver
from features import interfaces
from numpy import array
import unicodecsv as csv
import codecs
from nltk import sent_tokenize, word_tokenize


class TournamentDebatesObserver(IDebatesObserver):
    def __init__(self, features_extractors, online_audience_proportion=0.2):
        self.__features_extractors__ = features_extractors
        self.online_audience_proportion = online_audience_proportion
        self.__data__ = []
        self.__labels__ = []
        self.__names__ = []
        self.__speakers_names__ = []

        self.__has_paragraphs_features_extractor__ = False
        self.__has_sentences_features_extractor__ = False
        self.__has_tokens_features_extractor__ = False

        for fe in self.__features_extractors__:
            if isinstance(fe, interfaces.ParagraphsFeaturesExtractorBase):
                self.__has_paragraphs_features_extractor__ = True
            elif isinstance(fe, interfaces.SentencesFeaturesExtractorBase):
                self.__has_sentences_features_extractor__ = True
            elif isinstance(fe, interfaces.TokensListFeaturesExtractorBase):
                self.__has_tokens_features_extractor__ = True

    def observe(self, debate, name=None):
        for_motion_fv = []
        against_motion_fv = []
        label = self.__create_label__(debate)

        for speaker in debate.speakers:
            fv = self.__create_features_vector__(debate, speaker)
            (for_motion_fv if speaker.stand_for else against_motion_fv)\
                .append((speaker.name, fv))

        for for_name, for_fv in for_motion_fv:
            for against_name, against_fv in against_motion_fv:
                self.__data__.append(for_fv + against_fv)
                self.__speakers_names__.append((for_name, against_name))

        # fv that treats the speakers in each side as the same person
        self.__data__.append(self.__create_mutual_features_vector__(debate, True) +
                             self.__create_mutual_features_vector__(debate, False))
        self.__speakers_names__.append(('All speakers', 'All speakers'))

        num_records = (len(for_motion_fv) * len(against_motion_fv)) + 1

        self.__labels__ += [label] * num_records
        self.__names__ += [name] * num_records

    def digest(self):
        return array(self.__data__), array(self.__labels__)

    def export(self, path):
        with codecs.open(path, 'w', 'utf-8') as fh:
            wr = csv.writer(fh, quoting=csv.QUOTE_ALL, encoding='utf-8')

            # headers
            features_headers = []
            for extractor in self.__features_extractors__:
                features_headers += extractor.features_descriptions()

            headers = ['debate', 'for motion', 'against motion', 'label'] \
                      + ['(f) %s' % fh for fh in features_headers] \
                      + ['(a) %s' % fh for fh in features_headers]
            wr.writerow(headers)
            del headers

            for ind in range(len(self.__names__)):
                speakers = self.__speakers_names__[ind]

                row = [self.__names__[ind],
                       speakers[0], speakers[1],
                       self.__labels__[ind]] + self.__data__[ind]

                try:
                    wr.writerow(row)
                except Exception as e:
                    print('Failed to write row %d to csv.\nError: %s\nRow: %s' % (ind, str(e), row))

    def __create_features_vector__(self, debate, speaker):
        paragraphs = interfaces.ParagraphsFeaturesExtractorBase\
            .split_to_paragraphs(debate, speaker) if self.__has_paragraphs_features_extractor__ else None
        sentences = interfaces.SentencesFeaturesExtractorBase\
            .split_to_sentences(debate, speaker) if self.__has_sentences_features_extractor__ else None
        tokens = interfaces.TokensListFeaturesExtractorBase\
            .split_to_tokens(debate, speaker) if self.__has_tokens_features_extractor__ else None

        return self.__create_features_vector_inner_(debate, paragraphs, sentences, tokens)

    def __create_mutual_features_vector__(self, debate, stand_for):
        paragraphs = [p for p in debate.transcript_paragraphs
                      if p.speaker.stand_for == stand_for]
        sentences = [sent_tokenize(p.text) for p in paragraphs if not p.is_meta] \
            if self.__has_sentences_features_extractor__ else None
        tokens = [word_tokenize(p.text) for p in paragraphs if not p.is_meta] \
            if self.__has_tokens_features_extractor__ else None

        if not self.__has_paragraphs_features_extractor__:
            paragraphs = None

        return self.__create_features_vector_inner_(debate, paragraphs, sentences, tokens)

    def __create_features_vector_inner_(self, debate, paragraphs, sentences, tokens):
        features_vector = []
        for features_extractor in self.__features_extractors__:
            if isinstance(features_extractor, interfaces.ParagraphsFeaturesExtractorBase):
                features = features_extractor.extract_features_from_paragraphs(debate, paragraphs)
            elif isinstance(features_extractor, interfaces.SentencesFeaturesExtractorBase):
                features = features_extractor.extract_features_from_sentences(debate, sentences)
            elif isinstance(features_extractor, interfaces.TokensListFeaturesExtractorBase):
                features = features_extractor.extract_features_from_tokens(debate, tokens)
            else:
                print('Warning! tournament does not supports FeaturesExtractor that are not Paragraphs,'
                      ' Sentences or Tokens features extractors')
                continue

            features_vector += features

        return features_vector

    def __create_label__(self, debate):
        # the changes (in percentages) in for motion (in average between live and online audience)

        change = (self.online_audience_proportion * self.__calc_results_change__(debate.results.online_audience_results)) \
                 + ((1 - self.online_audience_proportion) * self.__calc_results_change__(debate.results.live_audience_results))

        # NOTE: should be integer number for classifier classes
        return int(change)

    @staticmethod
    def __calc_results_change__(results):
        return 100 * (results.after_debate_votes.for_the_motion - results.before_debate_votes.for_the_motion)\
               / float((results.before_debate_votes.for_the_motion))
