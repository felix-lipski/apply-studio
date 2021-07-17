from enum import Enum


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

