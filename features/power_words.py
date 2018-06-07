from interfaces import ParagraphsFeaturesExtractorBase


class PowerfulWordsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __default_list__ = [
        'might',
        'should',
        'shouldn\'t',
        'could',
        'couldnn\'t',
        'must',
        'would',
        'would\'nt',
        'biggest',
        'worst',
        'best'
        'worst'
        'ever',
        'never',
        # TODO: add more words!
    ]

    def __init__(self, words=None):
        self.__words__ = words if words else self.__default_list__

    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        powerful_count = 0
        total_count = 0

        for paragraph in paragraphs_list:
            for t in paragraph.as_tokens:
                token = t.lower()
                if token.isalpha():
                    total_count += 1
                    if token in self.__words__:
                        powerful_count += 1

        if total_count == 0:
            return [0]
        return [powerful_count / float(total_count)]

    def features_descriptions(self):
        return ['per. of powerful words']
