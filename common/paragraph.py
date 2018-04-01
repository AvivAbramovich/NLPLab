class Paragraph:
    def __init__(self, speaker, text, start_time, end_time=None, is_meta=False):
        self.text = text
        self.speaker = speaker
        self.is_meta = is_meta
        self.start_time = start_time
        self.end_time = end_time