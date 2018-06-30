from nlp_lab.evaluation.labeling.provider.base import ILabelProvider


class BinsChangeLabelsProvider(ILabelProvider):
    DEFAULT_BIN_SIZE = 20

    def __init__(self, base_label_provider, bin_size=DEFAULT_BIN_SIZE):
        """
        :param base_label_provider: an ILabelProvider object to use
        :param bin_size: int. the size of bins, for example: bin=10 => bins are ...-100,-90,-80....80, 90,100...
        """
        self.labels_provider = base_label_provider
        self.bin_size = bin_size

    def provide_label(self, results):
        res = self.labels_provider.provide_label(results)

        # floor to the closest bin
        _res = res - (res % self.bin_size)
        return _res
