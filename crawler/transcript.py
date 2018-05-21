from common.paragraph import Paragraph
from re import match

__time_regex__ = '(\d+:)?[0-9]{2}:[0-9]{2}'


def find_total_time(driver):
    res = None

    try:
        podcast_btn = driver.find_element_by_class_name('podcast-btn')

        if podcast_btn:
            podcast_btn.click()
            for div in driver.find_elements_by_class_name('node-podcast'):
                title_div = div.find_element_by_class_name('title-wrapper')
                if 'unedited' in title_div.text.lower():
                    for span in div.find_element_by_class_name('time').find_elements_by_tag_name('span'):
                        if match(__time_regex__, span.text):
                            time = span.text.split(':')
                            time.reverse()  # first seconds, then minutes, etc.
                            res = int(time[0]) + 60 * int(time[1])
                            if len(time) > 2:
                                res += 3600 * int(time[2])
                            if len(time) > 3:
                                print('Debug!')
    except Exception as e:
        print('Failed to find podcast: %s', str(e))

    return res


def find_transcript(driver, speakers):
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

    # TODO: last paragraphs have no end_time, need to parse this from the page
    # (for example, the podcast contains the total length)

    total_time = find_total_time(driver)
    if total_time:
        for paragraph in paragraphs:
            paragraph.end_time = total_time
    else:
        print('Failed to fetch transcript duration!')

    return transcript
