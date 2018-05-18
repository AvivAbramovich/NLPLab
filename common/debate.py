class Debate:
    def __init__(self, speakers, transcript_paragraphs, debate_results):
        self.speakers = speakers
        self.transcript_paragraphs = transcript_paragraphs
        self.debate_results = debate_results

    def enum_speaker_paragraphs(self, speaker, include_meta=True):
        for p in self.transcript_paragraphs:
            if p.speaker == speaker and (include_meta or not p.is_meta):
                yield p