from base import ILabelingSystem


class PlainLabelingSystem(ILabelingSystem):
    def __init__(self, label_provider, base_on_live_audience=True):
        """
        :param label_provider: a ILabelProvider object
        :param base_on_live_audience: bool. True: use only live audience results. False: use only online audience results
        """
        self.label_provider = label_provider
        self.base_on_live_audience = base_on_live_audience

    def create_label(self, debate_results):
        return self.label_provider.provide_label(
            debate_results.live_audience_results if self.base_on_live_audience
            else debate_results.online_audience_results
        )