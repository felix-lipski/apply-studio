from enum import Enum
from time import sleep
from csv  import reader

from ui import print_center_msg, display_lines, select_option


def check_generated(offer):
    with open('data/pdf/generated.csv', newline='') as csvfile:
        spamreader = reader(csvfile)
        if len(list(filter(lambda x: x[0] == offer["company"] and x[1] == offer["title"], spamreader))) > 0:
            return True
    return False


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
        obj["generated"] = check_generated(obj)
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
        obj["generated"] = check_generated(obj)
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
        obj["generated"] = check_generated(obj)
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
        obj["generated"] = check_generated(obj)
        offers.append(obj)
    return offers


def handle_offer_pracujpl(driver, term, offers, selection):
    el = offers[selection]["element"]
    regions = el.find_elements_by_class_name("offer-regions__port") + el.find_elements_by_class_name("offer-regions")
    regions = regions[0].find_elements_by_class_name("offer-regions__label")
    regions = list(map(
        lambda x: {"name": x.get_attribute('innerHTML'), "element": x}
        , regions))
    url = ""
    if len(regions) > 0:
        url = select_option(driver, term, regions)
    else:
        url = el.find_element_by_class_name("offer__info").find_element_by_class_name("offer-details__title-link").get_attribute('href')
    if url:
        offer = offers[selection]

        lines = ["", "", term.black_on_white(term.center(offer["title"])), term.black_on_white(term.center(offer["company"])),]
        if offer["quick"]:
            lines.append(term.blue("Quick Apply!"))
        lines.append("")
        print_center_msg(term, "Loading offer...", term.black_on_yellow)
        driver.get(url)
        panels = driver.find_elements_by_class_name("OfferView1PIsMp")
        for panel in panels:
            lists = panel.find_elements_by_tag_name("ul")
            if len(lists) == 0:
                for p in panel.find_elements_by_tag_name("p"):
                    lines.append(p.text)
            for lst in lists:
                ps = lst.find_elements_by_tag_name("p")
                for p in ps:
                    lines.append(p.text)
                if len(ps) == 0:
                    for li in lst.find_elements_by_tag_name("li"):
                        lines.append(li.text)
                lines.append("".ljust(term.width))
            lines.append("".ljust(term.width, "─"))
        lines.append("")
        lines.append("")

        display_lines(term, lines)
        print_center_msg(term, "Returning...", term.black_on_yellow)
        driver.back()
    return driver


class Board(Enum):
    PRACUJPL = {
            "name": "pracuj.pl", 
            "url": "https://www.pracuj.pl/praca/react;kw?rd=30&et=17",
            "offers_getter": get_offers_pracujpl,
            "offer_handler": handle_offer_pracujpl
            }
    NOFLUFFJOBS = {
            "name": "No Fluff Jobs", 
            "url": "https://nofluffjobs.com/pl/jobs/react?criteria=seniority%3Dtrainee,junior",
            "offers_getter": get_offers_nofluffjobs,
            "offer_handler": None
            }
    JUSTJOINIT = {
            "name": "Just Join IT", 
            "url": "https://justjoin.it/all/all/junior?q=React@category",
            "offers_getter": get_offers_justjoinit,
            "offer_handler": None
            }
    LINKEDIN = {
            "name": "LinkedIn", 
            "url": "https://www.linkedin.com/jobs/search/?f_E=1%2C2&keywords=React",
            "offers_getter": get_offers_linkedin,
            "offer_handler": None
            }

