from common.debate import Debate
from common.paragraph import Paragraph
from HelperStructure.ZipParagraph import ZipParagraph
from nltk import sent_tokenize


class ZipDebate(Debate):
    def __init__(self, debate):
        self.speakers = debate.speakers
        self.transcript_paragraphs = debate.transcript_paragraphs
        self.debate_results = debate.debate_results
        self.zipped_paragraphs = self.Zip(debate.transcript_paragraphs)

    def Zip(self, paragraphs):
        zip_paragraphs = []
        last_paragraph = Paragraph(None, '', None)
        new_paragraph = None
        for paragraph in paragraphs:
            if last_paragraph.speaker == paragraph.speaker and \
                last_paragraph.end_time == paragraph.end_time and \
                last_paragraph.start_time == paragraph.start_time:
                if paragraph.is_meta:
                    new_paragraph.crowd_reaction.append(paragraph.text)
                else:
                    new_paragraph.text += paragraph.text
            else:
                if new_paragraph is not None:
                    new_paragraph.list_sentences = sent_tokenize(new_paragraph.text)
                    zip_paragraphs.append(new_paragraph)
                new_paragraph = ZipParagraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time)
                last_paragraph = Paragraph(paragraph.speaker, paragraph.text, paragraph.start_time, paragraph.end_time,
                                           paragraph.is_meta)

        return zip_paragraphs

    def enum_speaker_zip_paragraphs(self, speaker, include_meta=True):
        for p in self.zipped_paragraphs:
            if p.speaker == speaker and (include_meta or not p.is_meta):
                yield p