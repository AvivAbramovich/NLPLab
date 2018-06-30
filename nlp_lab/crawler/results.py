from re import findall
from nlp_lab.common import Votes, Results, DebateResults


def find_debate_results(driver):
    root_div = driver.find_element_by_id('breakdown-wrapper')
    buttons_div = root_div.find_element_by_id('vote-source')
    live_audience_button = buttons_div.find_element_by_xpath('//li[@data-source="live"]')
    online_audience_button = buttons_div.find_element_by_xpath('//li[@data-source="online"]')

    live_audience_button.click()
    live_results = __parse_results__(root_div)
    online_audience_button.click()
    online_results = __parse_results__(root_div)

    return DebateResults(live_results, online_results)


def __parse_results__(root):
    percentage_regex = '\d+%'
    labels_div = root.find_element_by_id('chart-labels')
    before_votes = Votes()
    after_votes = Votes()
    for div in labels_div.find_elements_by_tag_name('div'):
        style = div.get_attribute('style')
        _class = div.get_attribute('class')
        percentage = int(findall(percentage_regex, div.text)[0][:-1])

        votes = before_votes if 'left' in style else after_votes
        if _class == 'aga':
            votes.against_the_motion = percentage
        elif _class == 'for':
            votes.for_the_motion = percentage
        elif _class == 'und':
            votes.undecided = percentage
        else:
            print('Unknown class "%s"' % _class)

    return Results(before_votes, after_votes)
