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


if __name__ == '__main__':
    from sys import argv
    # # TODO: just for test, the result should be formatted to schema
    # if len(argv) != 2:
    #     print('Usage: run.py <output directory path>')
    #     exit()

    sub_driver = Chrome()
    for debate_url in find_all_debates():
        try:
            debate = fetch_single_debate(debate_url, sub_driver)
        except Exception as e:
            print('Failed to parse "%s": %s' % (debate_url, e))
        else:
            print('Successfully parsed "%s"' % debate_url)
        # TODO: format to schema and then saved to file

