from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase


class QuotesStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        list_sentences = []
        list_quotes = []

        for paragraph in paragraphs_list:
            list_sentences.extend(paragraph.as_sentences)
            start_pt = paragraph.text.find("\"")
            end_pt = paragraph.text.find("\"", start_pt + 1)  # add one to skip the opening "

            if start_pt != -1 and end_pt != -1:
                quote = paragraph.text[start_pt + 1: end_pt + 1]  # add one to get the quote excluding the ""
                list_quotes.append(quote)

        quotes_num = len(list_quotes)
        total_quotes_len = sum(len(s) for s in list_quotes)
        avg_quote_len = 0 if quotes_num == 0 else total_quotes_len / quotes_num
        quotes_ratio = 0 if len(list_sentences) == 0 else quotes_num / len(list_sentences)

        return [quotes_num, total_quotes_len, avg_quote_len, quotes_ratio]

    def features_descriptions(self):
        return ['num. of sentences with quotes',
                'num. total quotes len in words'
                'avg quote len',
                'percent of sentences with quotes to all sentences']