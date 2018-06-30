from nlp_lab.features.interfaces.base import IFeaturesExtractor
from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase

import numpy as np
from nltk import pos_tag,word_tokenize


class TalkToTheAudienceFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __default_list__ = [
        'you',
        'yours'
        ]

    def __init__(self, words=None):
        self.__words__ = words if words else self.__default_list__

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        talk_to_sentences = 0
        total_sentences = 0
        for paragraph in paragraphs_list:
            for sentence in paragraph.as_sentences:
                total_sentences += 1
                pos_tagger = pos_tag(word_tokenize(sentence))
                for token in pos_tagger:
                    token_word = token[0].lower()
                    if token[0].isalpha():
                        if token_word in self.__words__ or token[1] == 'VBG':
                            talk_to_sentences += 1
                            break

        if total_sentences == 0:
            return [0,0]

        return [talk_to_sentences,
                talk_to_sentences / float(total_sentences)]

    def features_descriptions(self):
        return ['num. of talk to audience sentences phrases',
                'percent of talk to audience sentences to all sentences']