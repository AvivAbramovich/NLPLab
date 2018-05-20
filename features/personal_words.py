from features.tokens import TokensListFeaturesExtractorBase


class PersonalWordsFeaturesExtractor(TokensListFeaturesExtractorBase):
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

    def _extract_features_from_tokens_(self, tokens_lists_generator):
        personal_count = 0
        total_count = 0

        for l in tokens_lists_generator:
            for t in l:
                token = t.lower()
                if token.isalpha():
                    total_count += 1
                    if token in self.__words__:
                        personal_count += 1

        if total_count == 0:
            return [0]
        return [personal_count / float(total_count)]

