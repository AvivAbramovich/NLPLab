from .base import IFeaturesExtractor
from warnings import warn


class AudienceReactionsFeaturesExtractor(IFeaturesExtractor):
    def extract_features(self, debate, speaker):
        applause_count = 0
        laugh_count = 0
        affirmative_count = 0

        for p in debate.enum_speaker_paragraphs(speaker):
            if p.is_meta:
                t = p.text.lower().replace('.', '')
                if t in ['laughter', 'laughs']:
                    laugh_count += 1
                elif t == 'applause':
                    applause_count += 1
                elif t == 'affirmative':
                    affirmative_count += 1
                else:
                    warn('Unknown audience reaction "%s"' % p.text)

        return [applause_count, laugh_count, affirmative_count]

    def features_descriptions(self):
        return [
            "num. appluases",
            "num. laughter",
            "num. affirmatives"
        ]
