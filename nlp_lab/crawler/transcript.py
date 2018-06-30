from nlp_lab.common import Paragraph

__time_regex__ = '(\d+:)?[0-9]{2}:[0-9]{2}'


def find_transcript(driver, speakers, duration):
    driver.find_element_by_class_name('transcript-btn').click()
    transcript_ul = driver.find_element_by_id('transcript')

    last_speaker = None

    transcript = []
    paragraphs = []
    speakers_dict = {speaker.name: speaker for speaker in speakers}

    for li in transcript_ul.find_elements_by_tag_name('li'):
        start_time = int(li.get_attribute('data-stamp'))  # offset in seconds from the debate beginning
        text = li.find_element_by_class_name('text').text

        # set the end time of the last li paragraphs
        for paragraph in paragraphs:
            paragraph.end_time = start_time

        if start_time < 0:
            raise Exception('Start time is negative')

        paragraphs = []

        for pg in [pg.strip() for pg in text.split('\n')]:
            if pg:
                if pg.endswith(':'):
                    # current speaker name
                    last_speaker = speakers_dict.get(pg[:-1], None)
                elif pg.startswith('[') and pg.endswith(']'):
                    if last_speaker:
                        paragraphs.append(Paragraph(last_speaker, pg[1:-1].strip(), start_time, is_meta=True))
                else:
                    if last_speaker:
                        paragraphs.append(Paragraph(last_speaker, pg.strip(), start_time))

        transcript += paragraphs

    # last paragraphs have no end_time, so set the duration of the debate (by the video duration)
    for paragraph in paragraphs:
        paragraph.end_time = duration

    return transcript