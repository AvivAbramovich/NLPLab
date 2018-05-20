from nltk import word_tokenize, pos_tag, ne_chunk
from features.base import IFeaturesExtractor
from HelperStructure.ZipDebate import ZipDebate

sentence = "Mark Zuckeberg and John are loving in Florida."
a = ne_chunk(pos_tag(word_tokenize(sentence)))
if hasattr(a[0], '_label') and a[0]._label == 'PERSON':
    print('hey')
else:
    print('a')
print(ne_chunk(pos_tag(word_tokenize(sentence))))

class PersonStatisticsFeaturesExtractor(IFeaturesExtractor):
    __default_list__ = [
        '?',
        '!'
        # TODO: add more words!
    ]

    def __init__(self, special_marks = None):
        self.special_marks = special_marks if special_marks else self.__default_list__

    def extract_features(self, debate, speaker):

        zip_debate = ZipDebate(debate)
        list_sentences = []
        person_mentioned_sentences = []
        count_person = 0
        feature_vector = []

        for zip_paragraph in zip_debate.enum_speaker_zip_paragraphs(speaker):
            for sentence in zip_paragraph.list_sentences:
                ner_tagger = ne_chunk(pos_tag(word_tokenize(sentence)))
                for tag in ner_tagger:
                    if hasattr(tag, '_label') and tag._label == 'PERSON':
                        count_person += 1
                        if sentence not in person_mentioned_sentences:
                            person_mentioned_sentences.append(sentence)
            list_sentences.extend(zip_paragraph.list_sentences)

        return [count_person,
                len(person_mentioned_sentences),
                0 if len(person_mentioned_sentences) == 0 else count_person / len(person_mentioned_sentences),
                0 if len(list_sentences) == 0 else len(person_mentioned_sentences) / len(list_sentences)]



