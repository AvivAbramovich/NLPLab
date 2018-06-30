from nlp_lab.features.interfaces import ParagraphsFeaturesExtractorBase
from nltk import pos_tag


class PersonalWordsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __default_list__ = [
        'my',
        'own',
        'personal',
        'private',
        'privy',
        'mine',
        'I',
        'owned',
        # TODO: add more words!
    ]

    def __init__(self, words=None):
        self.__words__ = words if words else self.__default_list__

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        personal_count_sentences = 0
        total_sentences = 0

        for paragraph in paragraphs_list:
            for tokens in paragraph.as_sentences:
                total_sentences +=1
                pos_tagger = pos_tag(tokens)
                for token in pos_tagger:
                    token_word = token[0].lower()
                    if token[0].isalpha():
                        if token_word in self.__words__ or token[1] == 'VBD' or token[1] == 'VBN':
                            personal_count_sentences += 1
                            break

        if total_sentences == 0:
            return [0,0]
        return [personal_count_sentences,
                personal_count_sentences / float(total_sentences)]

    def features_descriptions(self):
        return ['num. of personal experiences sentences phrases',
                'percent of personal experiences sentences to all sentences']



