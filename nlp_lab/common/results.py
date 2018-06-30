class Votes:
    def __init__(self, for_the_motion=0, against_the_motion=0, undecided=0):
        self.for_the_motion = for_the_motion
        self.against_the_motion = against_the_motion
        self.undecided = undecided


class Results:
    def __init__(self, before_debate_votes, after_debate_votes):
        self.before_debate_votes = before_debate_votes
        self.after_debate_votes = after_debate_votes


class DebateResults:
    def __init__(self, live_audience_results, online_audience_results):
        self.live_audience_results = live_audience_results
        self.online_audience_results = online_audience_results