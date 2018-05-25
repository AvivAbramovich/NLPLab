from warnings import warn
from interfaces import ParagraphsFeaturesExtractorBase


class AudienceReactionsFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    __applause__ = 'applause'
    __affirmative__ = 'affirmative'
    __bell__ = 'bell'
    __ignore__ = [
        'inaudible',
        'unintelligible',
        'endoftranscript'
    ]
    __laughter__ = ['laughter', 'laughs']
    __speaking_simultaneously__ = 'simultaneous'

    def extract_features_from_paragraphs(self, _, paragraphs_list):
        applause_count = 0
        laugh_count = 0
        affirmative_count = 0
        bell_count = 0
        speaking_simultaneously_count = 0

        for p in paragraphs_list:
            if p.is_meta:
                t = p.text.lower().replace('.', '').replace(' ', '')
                flag = False

                # laughter
                for l in self.__laughter__:
                    if l in t:
                        laugh_count += 1
                        flag = True

                if self.__applause__ in t:
                    applause_count += 1
                    flag = True

                if self.__affirmative__ in t:
                    affirmative_count += 1
                    flag = True

                if self.__bell__ in t:
                    bell_count += 1
                    flag = True

                if self.__speaking_simultaneously__ in t:
                    speaking_simultaneously_count += 1
                    flag = True

                if not flag:
                    for i in self.__ignore__:
                        if i in t:
                            flag = True

                if not flag:
                    warn('Unknown audience reaction "%s"' % p.text)

        return [applause_count,
                laugh_count,
                affirmative_count,
                bell_count,
                speaking_simultaneously_count]

    def features_descriptions(self):
        return [
            "num. appluases",
            "num. laughter",
            "num. affirmatives",
            "num. bell rings",
            "num. speaking simultaneously"
        ]
