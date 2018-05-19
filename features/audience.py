from .base import IFeaturesExtractor


class AudienceReactionsFeaturesExtractor(IFeaturesExtractor):
    def extract_features(self, debate, speaker):
        applause_count = 0
        laugh_count = 0

        for p in debate.enum_speaker_paragraphs(speaker):
            if p.is_meta:
                if p.text == 'laughter':
                    laugh_count += 1
                elif p.text == 'applause':
                    applause_count += 1
                else:
                    pass

        return [applause_count, laugh_count]