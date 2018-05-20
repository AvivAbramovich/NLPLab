from features.base import IFeaturesExtractor, abstractmethod, ABCMeta
from HelperStructure.ZipDebate import ZipDebate


class QuotesStatisticsFeaturesExtractor(IFeaturesExtractor):

    def extract_features(self, debate, speaker):

        zip_debate = ZipDebate(debate)
        list_sentences = []
        list_quotes = []

        for zip_paragraph in zip_debate.enum_speaker_zip_paragraphs(speaker):
            start_pt = zip_paragraph.text.find("\"")
            end_pt = zip_paragraph.text.find("\"", start_pt + 1)  # add one to skip the opening "
            quote = zip_paragraph.text[start_pt + 1: end_pt + 1]  # add one to get the quote excluding the ""
            list_quotes.append(quote)
            list_sentences.extend(zip_paragraph.list_sentences)

        quotes_num = len(list_quotes)
        total_quotes_len = sum(len(s) for s in list_quotes)
        avg_quote_len = 0 if quotes_num == 0 else total_quotes_len / quotes_num
        quotes_ratio = 0 if len(list_sentences) == 0 else quotes_num / len(list_sentences)

        return [quotes_num, total_quotes_len, avg_quote_len, quotes_ratio]



