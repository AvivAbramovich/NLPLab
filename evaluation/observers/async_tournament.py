from evaluation.observers.base import IDebatesObserver
from features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase
from numpy import array
from time import time
from collections import defaultdict
import unicodecsv as csv
import codecs
from sys import stderr
from uuid import uuid1
from random import randint
from extra.jobs_executor import JobsExecutorBase, Locker


class JobExecutor(JobsExecutorBase):
    def __init__(self, num_threads, on_success_method, sleeping_time_in_seconds=3, queue_limit=500):
        super(JobExecutor, self).__init__(num_threads, sleeping_time_in_seconds, queue_limit)
        self.__on_success_method = on_success_method

    def generate_id(self):
        start_index = randint(0, 15)
        return str(uuid1()).replace('-', '')[start_index:start_index+10]

    def on_job_finished(self, _id, job, args, description, result):
        self.__on_success_method(result)


class TournamentDebatesAsyncObserver(IDebatesObserver):
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
        self.__jobs_executor__ = JobExecutor(10, self.__on_finish_debate__)

        for fe in self.__features_extractors__:
            if not isinstance(fe, ParagraphsFeaturesExtractorBase):
                raise Exception('%s supports only %s derived features extractors' %
                                (self.__class__.__name__, ParagraphsFeaturesExtractorBase.__class__.__name__))

    def observe(self, debate, name=None):
        # start new job
        self.__jobs_executor__.add_job(self.__observe_job__, (debate,name), name)

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

    def get_alternative_labels(self):
        """
        :return: an (n*d) numpy.array where n is the number of records and d is the number of alternative labeling systems
        """
        return array(self.__alternative_labels__)

    def __observe_job__(self, debate, name):
        # TODO: no write or change any self property, but return them, and the on_success change these properties with Lock
        for_motion_fv = []
        against_motion_fv = []

        # check if empty debate (crawler failed to parse the debate transcript)
        if len(debate.transcript_paragraphs) == 0:
            stderr.write('Debate %s has no transcript.\n' % ('"%s"' % name if name else ''))
            return

        time_stats = defaultdict(list)

        for speaker in debate.speakers:
            fv, stats = self.__create_features_vector__(debate, speaker, name)
            (for_motion_fv if speaker.stand_for else against_motion_fv) \
                .append((speaker.name, fv))
            for name, t in stats.items():
                time_stats[name].append(t)

        for for_name, for_fv in for_motion_fv:
            for against_name, against_fv in against_motion_fv:
                self.__data__.append(for_fv + against_fv)
                self.__speakers_names__.append((for_name, against_name))

        # fv that treats the speakers in each side as the same person
        for_values, for_stats = self.__create_mutual_features_vector__(debate, True, name)
        against_values, against_stats = self.__create_mutual_features_vector__(debate, False, name)

        self.__data__.append(for_values + against_values)
        for d in [for_stats, against_stats]:
            for name, t in d.items():
                time_stats[name].append(t)

        self.__speakers_names__.append(('All speakers', 'All speakers'))

        num_records = (len(for_motion_fv) * len(against_motion_fv)) + 1

        self.__labels__ += [self.__create_label__(debate)] * num_records
        if self.__alternative_labeling_systems__:
            self.__alternative_labels__ += [self.__create_alternative_labels__(debate)] * num_records
        self.__names__ += [name] * num_records

        return {n: (sum(tl) / float(len(tl))) for n, tl in time_stats.items()}

    def __on_finish_debate__(self, debate):
        # update the relevant properties
        with self.__locker__:
            raise NotImplementedError()

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
            self.__time_statistics__[features_extractor.__class__.__name__].append(t)
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
            self.__time_statistics__[features_extractor.__class__.__name__].append(t)
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