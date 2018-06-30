from nlp_lab.evaluation.observers.base import IDebatesObserver
from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase
from numpy import array
from time import time
from collections import defaultdict
import unicodecsv as csv
import codecs
from sys import stderr
from nlp_lab.extra.locker import Locker


class TournamentDebatesObserver(IDebatesObserver):
    def __init__(self, features_extractors, labeling_system, alternative_labeling_systems=None):

        self.__features_extractors__ = features_extractors
        self.__labeling_system__ = labeling_system
        self.__alternative_labeling_systems__ = alternative_labeling_systems
        self.__data__ = []
        self.__labels__ = []
        self.__names__ = []
        self.__speakers_names__ = []
        self.__alternative_labels__ = []
        self.__time_statistics__ = defaultdict(list)
        self.__locker__ = Locker()

        for fe in self.__features_extractors__:
            if not isinstance(fe, ParagraphsFeaturesExtractorBase):
                raise Exception('%s supports only %s derived features extractors' %
                                (self.__class__.__name__, ParagraphsFeaturesExtractorBase.__class__.__name__))

    def observe(self, debate, name=None):
        res = self.__observe_job__(debate, name)
        self.__on_finish_debate__((debate, name), res)
        return True

    def digest(self):
        return array(self.__data__), array(self.__labels__)

    def export(self, path):
        with codecs.open(path, 'w', 'utf-8') as fh:
            wr = csv.writer(fh, quoting=csv.QUOTE_ALL, encoding='utf-8')

            # headers
            features_headers = []
            for extractor in self.__features_extractors__:
                features_headers += extractor.features_descriptions()

            headers = ['debate', 'for motion', 'against motion', 'label']

            if self.__alternative_labeling_systems__:
                for i in range(len(self.__alternative_labeling_systems__)):
                    headers.append('Alt. label %d' % (i+1))

            headers += ['(f) %s' % fh for fh in features_headers] \
                       + ['(a) %s' % fh for fh in features_headers]
            wr.writerow(headers)
            del headers

            for ind in range(len(self.__names__)):
                speakers = self.__speakers_names__[ind]

                row = [self.__names__[ind],
                       speakers[0], speakers[1],
                       self.__labels__[ind]]

                if self.__alternative_labeling_systems__:
                    row += self.__alternative_labels__[ind]

                row += self.__data__[ind]

                try:
                    wr.writerow(row)
                except UnicodeDecodeError:
                    for ind, v in enumerate(row):
                        if type(v) in [str, unicode]:
                            # remove any not ascii character
                            row[ind] = ''.join([c for c in v if ord(c) < 128])
                    wr.writerow(row)
                except Exception as e:
                    print('Failed to write row %d to csv.\nError: %s\nRow: %s' % (ind, str(e), row))

    def get_features_descriptions(self):
        for fe in self.__features_extractors__:
            for desc in fe.features_descriptions():
                yield desc

    def get_alternative_labels(self):
        """
        :return: an (n*d) numpy.array where n is the number of records and d is the number of alternative labeling systems
        """
        return array(self.__alternative_labels__)

    def __observe_job__(self, debate, debate_name):
        # return properties
        data = []
        speakers_names = []
        time_stats = defaultdict(list)
        labels = []
        alt_labels = []
        names = []

        for_motion_fv = []
        against_motion_fv = []

        # check if empty debate (crawler failed to parse the debate transcript)
        if len(debate.transcript_paragraphs) == 0:
            stderr.write('Debate %s has no transcript.\n' % ('"%s"' % debate_name if debate_name else ''))
            return

        for speaker in debate.speakers:
            # debug
            # print('%s: create fv for %s' % (debate_name, speaker.name))
            #debug end
            fv, stats = self.__create_features_vector__(debate, speaker, debate_name)
            (for_motion_fv if speaker.stand_for else against_motion_fv) \
                .append((speaker.name, fv))
            for fv_name, t in stats.items():
                time_stats[fv_name].append(t)

        for for_name, for_fv in for_motion_fv:
            for against_name, against_fv in against_motion_fv:
                data.append(for_fv + against_fv)
                speakers_names.append((for_name, against_name))

        # fv that treats the speakers in each side as the same person
        for_values, for_stats = self.__create_mutual_features_vector__(debate, True, debate_name)
        against_values, against_stats = self.__create_mutual_features_vector__(debate, False, debate_name)

        data.append(for_values + against_values)
        for d in [for_stats, against_stats]:
            for fv_name, t in d.items():
                time_stats[fv_name].append(t)

        speakers_names.append(('All speakers', 'All speakers'))

        num_records = (len(for_motion_fv) * len(against_motion_fv)) + 1

        labels += [self.__create_label__(debate)] * num_records
        if self.__alternative_labeling_systems__:
            alt_labels += [self.__create_alternative_labels__(debate)] * num_records
        names += [debate_name] * num_records

        return data, speakers_names, time_stats, labels, alt_labels, names

    def __on_finish_debate__(self, args, res):
        # update the relevant properties
        with self.__locker__:
            # print('Finished "%s"' % args[1])
            data, speakers_names, time_stats, labels, alt_labels, names = res
            self.__data__ += data
            self.__speakers_names__ += speakers_names
            self.__labels__ += labels
            self.__alternative_labels__ += alt_labels
            self.__names__ += names

            for k, v in time_stats.items():
                self.__time_statistics__[k] += v

    def get_average_extractor_time(self):
        return {
            n:(sum(tl)/float(len(tl))) for n,tl in self.__time_statistics__.items()
        }

    def __create_features_vector__(self, debate, speaker, debate_name=None):
        features_vector = []
        time_stats = {}
        for features_extractor in self.__features_extractors__:
            start = time()
            features = features_extractor.extract_features(debate, speaker)
            t = time() - start
            time_stats[features_extractor.__class__.__name__] = t

            # check no negative values
            if any([value < 0 for value in features]):
                raise Exception('Feature extractor %s yield negative value(s)%s'
                                % (features_extractor.__class__.__name__,
                                   (' in "%s"' % debate_name) if debate_name else ''))
            features_vector += features

        return features_vector, time_stats

    def __create_mutual_features_vector__(self, debate, stand_for, debate_name=None):
        paragraphs = [p for p in debate.transcript_paragraphs
                      if p.speaker.stand_for == stand_for]

        features_vector = []
        time_stats = {}
        for features_extractor in self.__features_extractors__:
            start = time()
            features = features_extractor.extract_features_from_paragraphs(debate, paragraphs)
            t = time() - start
            time_stats[features_extractor.__class__.__name__] = t

            # check no negative values
            if any([value < 0 for value in features]):
                raise Exception('Feature extractor %s yield negative value(s)%s'
                                % (features_extractor.__class__.__name__,
                                   (' in "%s"' % debate_name) if debate_name else ''))

            features_vector += features

        return features_vector, time_stats

    def __create_label__(self, debate):
        return self.__labeling_system__.create_label(debate.results)

    def __create_alternative_labels__(self, debate):
        return [ls.create_label(debate.results) for ls in self.__alternative_labeling_systems__]