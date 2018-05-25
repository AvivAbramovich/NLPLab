from paragraph import Paragraph


class Debate:
    def __init__(self, speakers, transcript_paragraphs, debate_results):
        self.speakers = speakers
        self.transcript_paragraphs = transcript_paragraphs
        self.results = debate_results

    def enum_speaker_paragraphs(self, speaker, include_meta=True):
        for p in self.transcript_paragraphs:
            if p.speaker == speaker and (include_meta or not p.is_meta):
                yield p

    @property
    def total_time(self):
        return self.transcript_paragraphs[-1].end_time if len(self.transcript_paragraphs) > 0 else 0

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

        return Debate(self.speakers, new_paragraphs, self.results)