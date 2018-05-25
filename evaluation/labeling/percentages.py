from base import ILabelProvider


class PercentagesChangeLabelsProvider(ILabelProvider):
    def provide_label(self, results):
        # TODO: if before is 0%, then throw DivideByZero exception
        res = 100 * (results.after_debate_votes.for_the_motion - results.before_debate_votes.for_the_motion)\
               / float(results.before_debate_votes.for_the_motion)
        return int(res)