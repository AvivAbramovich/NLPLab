from abc import ABCMeta, abstractmethod
from nlp_lab.evaluation.observers.base import IDebatesObserver
from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase
from time import time
from collections import defaultdict
import unicodecsv as csv
import codecs
from nlp_lab.extra.locker import Locker
try:
    from numpy import array
except ImportError:
    assert 'numpy has no array object'


class SingleResult:
    def __init__(self, data, label, speaker_name, alternative_labels=None):
        self.data = data
        self.label = label
        self.alternative_labels = alternative_labels
        self.speaker_name = speaker_name


class ObservingResults:
    def __init__(self, results, time_stats, debate_name=None):
        self.debate_name = debate_name
        self.results = results
        self.time_stats = time_stats


class ITournamentDebatesObserverBase(IDebatesObserver):
    __metaclass__ = ABCMeta

    def __init__(self, debug_print=False):
        self.__data__ = []
        self.__labels__ = []
        self.__names__ = []
        self.__speakers_names__ = []
        self.__alternative_labels__ = []
        self.__time_statistics__ = defaultdict(list)
        self.__locker__ = Locker()
        self._debug_print_ = debug_print
        self.__print_locker__ = Locker()

    @abstractmethod
    def _do_observe_(self, debate, name):
        """
        Perform the debate processing and labeling
        :param debate: a Debate object
        :param name: the name of the debate
        :return: ObservingResults object
        """
        pass

    def observe(self, debate, name=None):
        observing_results = self._do_observe_(debate, name)
        self.__on_finish_debate__((debate, name), observing_results)
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

    def __on_finish_debate__(self, args, observing_results):
        # update the relevant properties
        if observing_results is not None:
            with self.__locker__:
                if self._debug_print_:
                    with self.__print_locker__:
                        print('Finished "%s"' % args[1])
                for result in observing_results.results:
                    self.__data__ += result.data
                    self.__speakers_names__ += result.speaker_name
                    self.__labels__ += result.label
                    self.__alternative_labels__ += result.alternative_labels
                    self.__names__ += observing_results.debate_name

                for k, v in observing_results.time_stats.items():
                    self.__time_statistics__[k] += v

    def get_average_extractor_time(self):
        return {
            n:(sum(tl)/float(len(tl))) for n,tl in self.__time_statistics__.items()
        }
