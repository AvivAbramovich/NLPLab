from common.speaker import Speaker
from warnings import warn


def find_speakers(driver):
    stand_for_div = None
    stand_against_div = None

    for div in driver.find_elements_by_class_name('stand'):
        classes = div.get_attribute('class')
        if 'stand-for' in classes:
            stand_for_div = div
        elif 'stand-against' in classes:
            stand_against_div = div

    if not stand_for_div:
        raise Exception('Failed to find "stand-for" div')
    if not stand_against_div:
        raise Exception('Failed to find "stand-against" div')

    return __parse_speakers__(stand_for_div) + __parse_speakers__(stand_against_div, False)


def __parse_speakers__(speakers_div, stand_for=True):
    return [__parse_speaker__(speaker_div, stand_for) for
            speaker_div in speakers_div.find_elements_by_class_name('speaker')]


def __parse_speaker__(speaker_div, stand_for=True):
    speaker_info_div = speaker_div.find_element_by_class_name('speaker-info')
    name = speaker_info_div.find_element_by_tag_name('h3').text
    try:
        description = speaker_info_div.find_element_by_class_name('even').text
    except:
        warn('Failed to fetch description for %s' % name)
        description = None
    try:
        bio = speaker_div.find_element_by_class_name('bio').text
    except:
        warn('Failed to fetch bio for %s' % name)
        bio = None

    return Speaker(name, stand_for, description, bio)
