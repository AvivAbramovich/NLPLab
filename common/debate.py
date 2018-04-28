class Debate:
    def __init__(self, speakers=None, transcript_paragraphs=[], debate_results = None):
        self.speakers = speakers
        self.transcript_paragraphs = transcript_paragraphs
        self.debate_results = debate_results

    def add_transcript_paragraph(self,paragraph):
        self.transcript_paragraphs.append(paragraph)
