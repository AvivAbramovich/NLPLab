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
            for sentence_as_pos_tokens in self.__paragraph_to_pos_tag_sentences_tokens__(paragraph):
                total_sentences +=1
                for token, tag in sentence_as_pos_tokens:
                    if token.isalpha() and (token.lower() in self.__words__ or tag in ['VBD', 'VBN']):
                            personal_count_sentences += 1
                            break

        if total_sentences == 0:
            return [0,0]
        return [personal_count_sentences,
                personal_count_sentences / float(total_sentences)]

    def features_descriptions(self):
        return ['num. of personal experiences sentences phrases',
                'percent of personal experiences sentences to all sentences']

    def __paragraph_to_pos_tag_sentences_tokens__(self, paragraph):
        sentences = [[]]
        for t in pos_tag(paragraph.as_tokens):
            if t[1] == '.':
                sentences.append([])
            else:
                sentences[-1].append(t)
        return sentences



