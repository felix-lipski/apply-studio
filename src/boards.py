from enum import Enum
from time import sleep


def get_offers_pracujpl(driver):
    offers = []
    fetched_offers = driver.find_elements_by_class_name("offer-details__text")
    for offer_element in fetched_offers:
        obj = {}
        obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
        obj["company"] = (offer_element.find_element_by_class_name("offer-company__name").text)
        obj["element"] = offer_element.find_element_by_xpath("../../..")
        quick_apply = obj["element"].find_element_by_class_name("offer__info").find_elements_by_class_name("offer-labels__item--one-click-apply")
        obj["quick"] = len(quick_apply) > 0
        offers.append(obj)
    return offers


def get_offers_nofluffjobs(driver):
    offers = []
    fetched_offers = driver.find_elements_by_class_name("posting-list-item")
    for offer_element in fetched_offers:
        obj = {}
        obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
        obj["company"] = (offer_element.find_element_by_class_name("company").text)
        obj["element"] = offer_element
        obj["quick"] = False
        offers.append(obj)
    return offers


def get_offers_justjoinit(driver):
    sleep(1)
    offers = []
    fetched_offers = driver.find_elements_by_class_name("jss218")
    for offer_element in fetched_offers:
        obj = {}
        obj["title"] = (offer_element
                .find_element_by_tag_name("img")
                .get_attribute('alt'))
        a = offer_element.find_element_by_xpath("..")
        obj["url"] = a.get_attribute("href")
        obj["company"] = obj["url"][27:]
        obj["element"] = offer_element
        obj["quick"] = False
        offers.append(obj)
    return offers


def get_offers_linkedin(driver):
    offers = []
    for i in range(4):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight*" + str((i + 1) / 4.0) + ")")
    sleep(1)
    fetched_offers       = driver.find_elements_by_class_name("jobs-search-results__list-item")
    for offer_element in fetched_offers:
        obj = {}
        n   = (len(offer_element.find_elements_by_class_name("job-card-list__title")))
        obj["title"]     = str(len(offer_element.find_elements_by_class_name("job-card-list__title")))
        if n > 0:
            obj["title"] = (offer_element.find_element_by_class_name("job-card-list__title").text)
        obj["company"]   = offer_element.find_element_by_class_name("job-card-container__company-name").text
        obj["element"]   = offer_element
        quick_apply = obj["element"].find_element_by_class_name("job-card-list__footer-wrapper").find_elements_by_class_name("job-card-container__apply-method")
        obj["quick"] = len(quick_apply) > 0
        offers.append(obj)
    return offers


class Board(Enum):
    PRACUJPL = {
            "name": "pracuj.pl", 
            "url": "https://www.pracuj.pl/praca/react;kw?rd=30&et=17",
            "offers_getter": get_offers_pracujpl
            }
    NOFLUFFJOBS = {
            "name": "No Fluff Jobs", 
            "url": "https://nofluffjobs.com/pl/jobs/react?criteria=seniority%3Dtrainee,junior",
            "offers_getter": get_offers_nofluffjobs
            }
    JUSTJOINIT = {
            "name": "Just Join IT", 
            "url": "https://justjoin.it/all/all/junior?q=React@category",
            "offers_getter": get_offers_justjoinit
            }
    LINKEDIN = {
            "name": "LinkedIn", 
            "url": "https://www.linkedin.com/jobs/search/?f_E=1%2C2&keywords=React",
            "offers_getter": get_offers_linkedin
            }

