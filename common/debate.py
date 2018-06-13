from common.paragraph import Paragraph


class Debate:
    def __init__(self, speakers, transcript_paragraphs, debate_results, duration):
        """
        :param speakers: list of common.speakers.Speaker objects
        :param transcript_paragraphs: list of common.paragraph.Paragraph objects
        :param debate_results: a common.results.DebateResults object
        :param duration: the duration of the debate (in seconds)
        """
        self.speakers = speakers
        self.transcript_paragraphs = transcript_paragraphs
        self.results = debate_results
        self.duration = duration

    def enum_speaker_paragraphs(self, speaker, include_meta=True):
        for p in self.transcript_paragraphs:
            if p.speaker == speaker and (include_meta or not p.is_meta):
                yield p

    def zip(self):
        """
        Create new Debate object which unify adjacent paragraph by the same speaker
        :return: new Debate object
        """

        new_paragraphs = []
        last_paragraph = None
        for paragraph in self.transcript_paragraphs:
            if last_paragraph and last_paragraph.speaker == paragraph.speaker and \
                    last_paragraph.start_time == paragraph.start_time and\
                    not (last_paragraph.is_meta or paragraph.is_meta):
                    last_paragraph.text += ' ' + paragraph.text
            else:
                last_paragraph = Paragraph(paragraph.speaker, paragraph.text,
                          paragraph.start_time, paragraph.end_time,
                          paragraph.is_meta)
                new_paragraphs.append(last_paragraph)

        return Debate(self.speakers, new_paragraphs, self.results, self.duration)