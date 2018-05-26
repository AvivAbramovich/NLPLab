from xml.etree.cElementTree import Element, SubElement, ElementTree


def dump_debate(debate, path, url=None):
    root = Element('debate')
    root.set('duration', debate.duration)
    if url:
        root.set('url', url)

    # speakers
    speakers_element = SubElement(root, 'speakers')
    for speaker in debate.speakers:
        speaker_element = SubElement(speakers_element, 'speaker')
        speaker_element.set('name', speaker.name)
        speaker_element.set('position', 'for' if speaker.stand_for else 'against')
        if speaker.description:
            desc_element = SubElement(speaker_element, 'description')
            desc_element.text = speaker.description

        if speaker.bio:
            bio_element = SubElement(speaker_element, 'bio')
            bio_element.text = speaker.bio

    # results
    __add_results__(root, debate.debate_results)

    # transcript
    transcript_element = SubElement(root, 'transcript')
    for paragraph in debate.transcript_paragraphs:
        p_element = SubElement(transcript_element, 'p')
        p_element.text = paragraph.text
        p_element.set('start', str(paragraph.start_time))
        p_element.set('is_meta', str(paragraph.is_meta).lower())
        p_element.set('speaker', paragraph.speaker.name)

        if paragraph.end_time:
            p_element.set('end', str(paragraph.end_time))

    ElementTree(root).write(path)


def __add_results__(root, result):
    results_element = SubElement(root, 'results')
    __add_result__(results_element, result.live_audience_results, 'live')
    __add_result__(results_element, result.online_audience_results, 'online')


def __add_result__(results_element, result, submitters):
    __add_votes__(SubElement(results_element, 'result'), 'before', submitters, result.before_debate_votes)
    __add_votes__(SubElement(results_element, 'result'), 'after', submitters, result.after_debate_votes)


def __add_votes__(result_element, when, submitters, votes):
    result_element.set('when', when)
    result_element.set('submitters', submitters)

    if votes.for_the_motion:
        result_element.set('for', str(votes.for_the_motion))
    if votes.against_the_motion:
        result_element.set('against', str(votes.against_the_motion))
    if votes.undecided:
        result_element.set('undecided', str(votes.undecided))
