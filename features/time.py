from .base import IFeaturesExtractor
from nltk import sent_tokenize


class SpeakingTimeFeaturesExtractor(IFeaturesExtractor):
    def extract_features(self, debate, speaker):
        total_speaking_time = 0
        last_paragraph_time_start = -1
        num_paragraphs = 0
        num_sentences = 0  # for proportion of num sentences, we need the other speakers num sentences.
                           # for now, just avg. sentences for p and for time

        for p in debate.enum_speaker_paragraphs(speaker):
            num_paragraphs += 1
            num_sentences += len(sent_tokenize(p.text))

            if not p.is_meta and p.start_time != last_paragraph_time_start:
                total_speaking_time += p.end_time - p.start_time
                last_paragraph_time_start = p.start_time

        if num_paragraphs == 0:
            return len(self.features_descriptions()) * [0]

        return [
            total_speaking_time / float(debate.total_time),
            num_paragraphs / float(len(debate.transcript_paragraphs)),
            num_sentences / float(num_paragraphs),
            float(debate.total_time) / num_sentences
        ]

    def features_descriptions(self):
        return [
            'per. speaking time',
            'per. paragraphs',
            'avg. sentences for paragraph',
            'avg. seconds for sentence'
        ]