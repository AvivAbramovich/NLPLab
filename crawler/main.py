# example source: https://sites.google.com/a/chromium.org/chromedriver/getting-started

from selenium.webdriver import Chrome
from time import sleep

from common.debate import Debate

from crawler.results import find_debate_results
from crawler.transcript import find_transcript
from crawler.speakers import find_speakers


def fetch_single_debate(url, driver=None):
    if not driver:
        driver = Chrome()
        close = True
    else:
        close = False

    driver.get(url)

    # get the speakers
    speakers = find_speakers(driver)

    # get results
    results = find_debate_results(driver)

    # transcript
    transcript = find_transcript(driver, speakers)

    if close:
        driver.close()
    return Debate(speakers, transcript, results)


def find_all_debates():
    base_url = 'https://www.intelligencesquaredus.org/debates'
    driver = Chrome()
    driver.get(base_url)
    driver.maximize_window()  # just to be easier to debug

    years_ul = driver.find_element_by_class_name('years')
    for year_li in years_ul.find_elements_by_class_name('year'):
        sleep(1)

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
                    yield debate_link
