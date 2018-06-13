from nltk import word_tokenize, pos_tag, ne_chunk
from features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase


class PersonStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        list_sentences = []
        person_mentioned_sentences = []
        count_person = 0

        for paragraph in paragraphs_list:
            for sentence in paragraph.as_sentences:
                ner_tagger = ne_chunk(pos_tag(word_tokenize(sentence)))
                for tag in ner_tagger:
                    if hasattr(tag, '_label') and tag._label == 'PERSON':
                        count_person += 1
                        if sentence not in person_mentioned_sentences:
                            person_mentioned_sentences.append(sentence)
            list_sentences.extend(paragraph.as_sentences)

        return [count_person,
                len(person_mentioned_sentences),
                0 if len(person_mentioned_sentences) == 0 else count_person / len(person_mentioned_sentences),
                0 if len(list_sentences) == 0 else len(person_mentioned_sentences) / len(list_sentences)]

    def features_descriptions(self):
        return ['num. of person mentioned',
                'num. of sentences with person mentioned',
                'avg. persons mentioned in the sentences',
                'precent. person mentioned sentences to all sentences']