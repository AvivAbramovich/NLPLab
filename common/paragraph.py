class Paragraph:
    def __init__(self, speaker, text, start_time, end_time=None, is_meta=False):
        self.text = text
        self.speaker = speaker
        self.is_meta = is_meta
        self.start_time = start_time
        self.end_time = end_time

    @property
    def as_sentences(self):
        # Lazy initialization
        try:
            return self.__sentences__
        except AttributeError:
            from nltk import sent_tokenize
            self.__sentences__ = sent_tokenize(self.text)
            return self.__sentences__

    @property
    def as_tokens(self):
        # Lazy initialization
        try:
            return self.__tokens__
        except AttributeError:
            from nltk import word_tokenize
            self.__tokens__ = word_tokenize(self.text)
            return self.__tokens__