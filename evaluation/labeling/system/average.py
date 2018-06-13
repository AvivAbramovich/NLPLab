from evaluation.labeling.system.base import ILabelingSystem


class AverageLabelingSystem(ILabelingSystem):
    DEFAULT_ONLINE_AUDIENCE_PROPORTION = 0.2

    def __init__(self, label_provider, online_audience_proportion=DEFAULT_ONLINE_AUDIENCE_PROPORTION):
        self.label_provider = label_provider
        self.online_audience_proportion = online_audience_proportion

    def create_label(self, debate_results):
        online = self.online_audience_proportion * self.label_provider.provide_label(debate_results.online_audience_results)
        live = (1 - self.online_audience_proportion) * self.label_provider.provide_label(debate_results.live_audience_results)

        return int(float(online + live)/2)
