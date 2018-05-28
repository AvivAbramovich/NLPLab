from xml.etree import ElementTree as ET
from common import *


def parse_file(file_path):
    return __parse__(ET.parse(file_path))


def parse_string(string):
    return __parse__(ET.fromstring(string))


def __parse__(root):
    duration = __parse_duration__(root)

    speakers = __parse_speakers__(root)

    results = __parse_results__(root)

    transcript = __parse_transcript__(root, speakers)

    return Debate(speakers, transcript, results, duration)


def __parse_duration__(root):
    return int(root.getroot().attrib['duration'])


def __parse_speakers__(root):
    return [__parse_speaker__(speaker_element) for speaker_element in root.find('speakers')]


def __parse_speaker__(speaker_element):
    name = speaker_element.attrib['name']
    for_motion = speaker_element.attrib['position'] == 'for'
    desc_elem = speaker_element.find('description')
    bio_elem = speaker_element.find('bio')

    desc = desc_elem.text if len(desc_elem) else None
    bio = bio_elem.text if len(bio_elem) else None

    return Speaker(name, for_motion, desc, bio)


def __parse_results__(root):
    live_results = Results(None, None)
    online_results = Results(None, None)

    for submitters, when, votes in \
        [__parse_result__(result_element) for result_element in root.find('results')]:

        results = live_results if submitters == 'live' else online_results
        if when == 'before':
            results.before_debate_votes = votes
        else:
            results.after_debate_votes = votes

    return DebateResults(live_results, online_results)


def __parse_result__(result_element):
    votes = Votes()

    if 'for' in result_element.attrib:
        votes.for_the_motion = int(result_element.attrib['for'])

    if 'against' in result_element.attrib:
        votes.against_the_motion = int(result_element.attrib['against'])

    if 'undecided' in result_element.attrib:
        votes.undecided = int(result_element.attrib['undecided'])

    return result_element.get('submitters'), \
           result_element.get('when'), \
           votes


def __parse_transcript__(root, speakers):
    speakers_dict = {s.name: s for s in speakers}
    return [__parse_paragraph__(p_element, speakers_dict) for p_element in root.find('transcript')]


def __parse_paragraph__(p_element, speakers_dict):
    speaker = speakers_dict[p_element.get('speaker')]
    text = p_element.text
    is_meta = p_element.get('is_meta').lower() == 'true'
    start = int(p_element.get('start')) if 'start' in p_element.attrib else None
    end = int(p_element.get('end')) if 'end' in p_element.attrib else None

    return Paragraph(speaker, text, start, end, is_meta)
