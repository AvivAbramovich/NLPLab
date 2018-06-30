from nlp_lab.evaluation.labeling.provider.base import ILabelProvider


class PercentagesChangeLabelsProvider(ILabelProvider):
    def provide_label(self, results):
        # TODO: if before is 0%, change to 1 to prevent divide by zero
        divider = results.before_debate_votes.for_the_motion if results.before_debate_votes.for_the_motion != 0 else 1

        res = 100 * (results.after_debate_votes.for_the_motion - divider) / float(divider)
        return int(res)