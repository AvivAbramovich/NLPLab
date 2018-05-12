from common import Debate
from common import Results
from Features.FeatureParagraph import FeatureParagraph

features = ['words_avg_in_sentence',
            'words_avg_in_time',
            'word_sentences_in_time',
            'real_words_feature',
            #'person_mentioned',
            'is_personal_experience',
            'is_insecure',
            'has_quote']


class FeatureDebate:
    def __init__(self, debate):
        self.debate = debate
        self.is_for_motion_won = self.is_for_won()
        self.feature_paragraphs = self.create_paras()

    def create_paras(self):

        feature_paragraphs = []
        try:
            for paragraph in self.debate.transcript_paragraphs:
                feature_paragraphs.append(FeatureParagraph(paragraph,
                                                           self.set_label(paragraph.speaker.stand_for),
                                                           features))
        except:
            feature_paragraphs = []

        return feature_paragraphs

    def set_label(self, paragraph_is_for_motion):
        if paragraph_is_for_motion == self.is_for_motion_won:
            return 1
        else:
            return 0

    def is_for_won(self):
        before_percent_against = self.debate.debate_results.live_audience_results.before_debate_votes.against_the_motion
        after_percent_against = self.debate.debate_results.live_audience_results.after_debate_votes.against_the_motion
        before_percent_for = self.debate.debate_results.live_audience_results.before_debate_votes.for_the_motion
        after_percent_for = self.debate.debate_results.live_audience_results.after_debate_votes.for_the_motion

        return after_percent_for - before_percent_for > after_percent_against - before_percent_against
