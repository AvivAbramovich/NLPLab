from nltk import Tree
from nlp_lab.features.interfaces.paragraphs import ParagraphsFeaturesExtractorBase


class PersonStatisticsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        person_mentioned_count = 0
        count_person = 0
        count_sentences = 0

        for paragraph in paragraphs_list:
            for sentence in self.__split_ne_by_sentences__(paragraph.as_ne_chunk):
                count_sentences += 1
                flag = True
                for tag in sentence:
                    if isinstance(tag, Tree) and tag.label() == 'PERSON':
                        count_person += 1
                        if flag:
                            flag = False
                            person_mentioned_count += 1

        return [count_person,
                person_mentioned_count,
                0 if person_mentioned_count == 0 else count_person / person_mentioned_count,
                0 if count_sentences == 0 else person_mentioned_count / count_sentences]

    def features_descriptions(self):
        return ['num. of person mentioned',
                'num. of sentences with person mentioned',
                'avg. persons mentioned in the sentences',
                'percent. person mentioned sentences to all sentences']

    @staticmethod
    def __split_ne_by_sentences__(ne_chunks):
        l = []
        for tag in ne_chunks:
            if isinstance(tag, tuple) and tag[1] == '.':
                if l:
                    yield l
                l = []
            else:
                l.append(tag)
        if l:
            yield l
