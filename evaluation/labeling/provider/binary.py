from evaluation.labeling.provider.base import ILabelProvider


class BinaryLabelProvider(ILabelProvider):
    def provide_label(self, results):
        """
        :param results: a common.results.Results object
        :return: 1 if the "for the motion" won, 0 otherwise
        """
        return int(results.after_debate_votes.for_the_motion > results.after_debate_votes.against_the_motion)
