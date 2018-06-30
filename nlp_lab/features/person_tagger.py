from nltk import pos_tag, ne_chunk
from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase


class PersonStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        list_sentences = []
        person_mentioned_sentences_count = 0
        count_person = 0

        for paragraph in paragraphs_list:
            for tokens in paragraph.as_tokens:
                flag = False
                ner_tagger = ne_chunk(pos_tag(tokens))
                for tag in ner_tagger:
                    if hasattr(tag, '_label') and tag._label == 'PERSON':
                        count_person += 1
                        if not flag:
                            flag = True
                            person_mentioned_sentences_count += 1
            list_sentences.extend(paragraph.as_sentences)

        return [count_person,
                person_mentioned_sentences_count,
                0 if person_mentioned_sentences_count == 0 else count_person / person_mentioned_sentences_count,
                0 if len(list_sentences) == 0 else person_mentioned_sentences_count / len(list_sentences)]

    def features_descriptions(self):
        return ['num. of person mentioned',
                'num. of sentences with person mentioned',
                'avg. persons mentioned in the sentences',
                'precent. person mentioned sentences to all sentences']