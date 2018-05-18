from .tokens import TokensListFeaturesExtractorBase


class PowerfullWordsFeaturesExtractor(TokensListFeaturesExtractorBase):
    __default_list__ = [
        'might',
        'should',
        'shouldn\'t',
        'could',
        'couldnn\'t',
        'must',
        # TODO: add more words!
    ]

    def __init__(self, words=None):
        self.__words__ = words if words else self.__default_list__

    def _extract_features_from_tokens_(self, tokens_lists_generator):
        powerful_count = 0
        total_count = 0

        for l in tokens_lists_generator:
            for t in l:
                token = t.lower()
                if token.isalpha():
                    total_count += 1
                    if token in self.__words__:
                        powerful_count += 1

        if total_count == 0:
            return [0]
        return [powerful_count / float(total_count)]

