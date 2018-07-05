# example source: https://sites.google.com/a/chromium.org/chromedriver/getting-started

from time import sleep
from warnings import warn

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

from duration import find_duration
from nlp_lab.common import Debate
from results import find_debate_results
from speakers import find_speakers
from transcript import find_transcript, find_transcript_button


def fetch_single_debate(url, driver=None):
    if not driver:
        driver = Chrome()
        close = True
    else:
        close = False

    print('Start crawling "%s"' % url)
    try:
        driver.get(url)

        sleep(5)  # wait the page to fully load

        # start by seek the transcript button, is not exists, no use for this debate...
        try:
            find_transcript_button(driver)
        except NoSuchElementException:
            raise Exception('The debate has no transcript, aborting')

        try:
            duration = find_duration(driver)
            for i in range(15):
                print('Duration is 0, wait 3 seconds and then check again...')
                sleep(3)
                duration = find_duration(driver)
                if duration != 0:
                    break
            if duration == 0:
                raise Exception('TimeOut')
        except Exception as e:
            warn('Failed to fetch duration to "%s": %s' % (url, e.message))
            duration = -1

        # get the speakers
        speakers = find_speakers(driver)

        # get results
        results = find_debate_results(driver)

        # transcript
        transcript = find_transcript(driver, speakers, duration)

        return Debate(speakers, transcript, results, duration)

    finally:
        if close:
            driver.close()


def find_all_debates(driver=None, base_url=None):
    if not base_url:
        base_url = 'https://www.intelligencesquaredus.org/debates'

    if not driver:
        driver = Chrome()

    driver.get(base_url)
    driver.maximize_window()  # just to be easier to debug

    years_ul = driver.find_element_by_class_name('years')
    for year_li in years_ul.find_elements_by_class_name('year'):
        sleep(3)

        # check if the pop up appear
        try:
            pop_up_div = driver.find_element_by_id('modalContent')
        except:
            pass
        else:
            pop_up_div.find_element_by_class_name('modal-header').find_element_by_tag_name('a').click()

        print('year: %s' % year_li.text.split()[0])
        year_li.click()
        for month_li in year_li.find_elements_by_class_name('month'):
            # search for the month with "All" as text
            if month_li.find_element_by_tag_name('label').text == 'All':
                sleep(1)

                # open all the debates
                month_li.click()

                sleep(1)

                for debate_aside in driver.find_element_by_class_name('debates-list')\
                        .find_elements_by_class_name('node-debate'):
                    debate_link = debate_aside.find_element_by_class_name('field-name-title')\
                        .find_element_by_tag_name('a')\
                        .get_attribute('href')
                    if debate_link.split('/')[-1].split('-')[0] != 'unresolved':
                        yield debate_link
