from interfaces import TokensListFeaturesExtractorBase


class PowerfulWordsFeaturesExtractor(TokensListFeaturesExtractorBase):
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

    def extract_features_from_tokens(self, tokens_lists_list):
        powerful_count = 0
        total_count = 0

        for l in tokens_lists_list:
            for t in l:
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
