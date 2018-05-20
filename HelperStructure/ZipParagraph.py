class ZipParagraph:
    def __init__(self, speaker, text, start_time, end_time=None):
        self.text = text
        self.list_sentences = []
        self.speaker = speaker
        self.start_time = start_time
        self.end_time = end_time
        self.crowd_reaction = []