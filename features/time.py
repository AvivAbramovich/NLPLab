from interfaces import ParagraphsFeaturesExtractorBase


class ParagraphsSpeakingTimeFeaturesExtractor(ParagraphsFeaturesExtractorBase):
    def extract_features_from_paragraphs(self, debate, paragraphs_list):
        total_speaking_time = 0
        last_paragraph_time_start = -1
        num_paragraphs = 0

        for p in paragraphs_list:
            num_paragraphs += 1

            if not p.is_meta and p.start_time != last_paragraph_time_start:
                total_speaking_time += p.end_time - p.start_time
                last_paragraph_time_start = p.start_time

        if num_paragraphs == 0:
            return len(self.features_descriptions()) * [0]

        # return [
        #     total_speaking_time / float(debate.duration),
        #     num_paragraphs / float(len([p for p in debate.transcript_paragraphs if not p.is_meta])),
        # ]

        res = [
            total_speaking_time / float(debate.duration),
            num_paragraphs / float(len([p for p in debate.transcript_paragraphs if not p.is_meta])),
        ]

        if any([i < 0 for i in res]):
            pass

        return res


    def features_descriptions(self):
        return [
            'per. speaking time',
            'per. paragraphs',
        ]
