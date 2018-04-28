class Paragraph:
    def __init__(self, speaker, text, start_time, end_time=None, is_meta=False):
        self.text = text
        self.speaker = speaker
        self.is_meta = is_meta
        self.start_time = start_time
        self.end_time = end_time
        self.sentences = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.speaker == other.speaker and self.start_time == other.start_time and self.end_time == other.end_time and self.is_meta == other.is_meta
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)