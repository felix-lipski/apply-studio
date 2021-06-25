from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from blessed import Terminal

from browse import load_browser
from graphics import print_center_msg

def get_offers(driver, company = "pracuj.pl"):
    offers = []
    if company == "pracuj.pl":
        # fetched_offers = driver.find_elements_by_class_name("results__list-container-item")
        fetched_offers = driver.find_elements_by_class_name("offer-details__text")
        for offer_element in fetched_offers:
            obj = {}
            # offer_details_element = offer_element.find_element_by_class_name("offer-details__text")
            obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
            obj["company"] = (offer_element.find_element_by_class_name("offer-company__name").text)
            obj["element"] = offer_element.find_element_by_xpath("../../..")
            offers.append(obj)
    return offers


def input_loop(term, offline = False, headless = False):
    driver = 0
    offers = []
    if offline == False:
        driver = load_browser(term, headless = headless)
        offers = get_offers(driver)
    else:
        offers = [
                {"company": "first company", "title": "first job"},
                {"company": "second company", "title": "second job"},
                {"company": "third company", "title": "third company"},
                {"company": "quix", "title": "man"},
                {"company": "fooa", "title": "janitor"},
                {"company": "barr", "title": "monitor"},
                {"company": "baze", "title": "clerk"},
                {"company": "quiz", "title": "man"},
                {"company": "fooa1", "title": "janitor"},
                {"company": "barr1", "title": "monitor"},
                {"company": "baze1", "title": "clerk"},
                {"company": "quiz1", "title": "man"},
                {"company": "fooa2", "title": "janitor"},
                {"company": "barr2", "title": "monitor"},
                {"company": "baze2", "title": "clerk"},
                {"company": "quiz2", "title": "man"},
                {"company": "fooa11", "title": "janitor"},
                {"company": "barr11", "title": "monitor"},
                {"company": "baze11", "title": "clerk"},
                {"company": "quiz11", "title": "man"},
                {"company": "fooa21", "title": "janitor"},
                {"company": "barr21", "title": "monitor"},
                {"company": "baze21", "title": "clerk"},
                {"company": "quiz21", "title": "man"},
                {"company": "fooa12", "title": "janitor"},
                {"company": "barr12", "title": "monitor"},
                {"company": "baze12", "title": "clerk"},
                {"company": "quiz12", "title": "man"},
                {"company": "fooa22", "title": "janitor"},
                {"company": "third to last company", "title": "third to last job"},
                {"company": "second to last company", "title": "second to last job"},
                {"company": "last company", "title": "last job"},
                ]
    selection = 0
    scroll = 0
    offer_height = 3
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        val = ""
        while val.lower() != "q":
            print_offers(term, offers, selection, scroll)
            val = term.inkey()
            if not val:
                pass
              # print("It sure is quiet in here ...")
            elif val.is_sequence:
                # print("got sequence: {0}.".format((str(val), val.name, val.code)))
                if val.name == "KEY_ENTER":
                    print("enter")
                    # offers[selection]["element"].find_element_by_class_name
                # if val.name == "KEY_ESCAPE":
            elif val:
                if val == "j":
                    selection = min(selection + 1, max(len(offers) - 1, 0))
                    if (selection*offer_height) >= term.height - 8:
                        scroll = min(scroll+offer_height, (len(offers) + 2) * offer_height - term.height)
                    
                if val == "k":
                    selection = max(selection - 1, 0)
                    if (selection*offer_height) - scroll <= 4:
                        scroll = max(scroll-offer_height, 0)
                if val == "r":
                    driver.get("https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
        print(f'bye!{term.normal}')



def print_offers(term, offers, selection, scroll):
    width = 60
    lines = []
    for i, offer in enumerate(offers):
        title = (" " + offer["title"]).ljust(width)[:width]
        company = ((offer["company"]).ljust(width))[:width]
        if i == selection:
            title = (term.black_on_white(title))
            company = (term.black_on_white(company))
        lines.append((title))
        lines.append((company))
        lines.append("".ljust(width))

    print(term.home)
    for i in range(term.height - 6):
        pos = i + (scroll)
        pos_str = ""
        # pos_str = str(pos)
        if scroll <= pos < term.height - 6 + scroll and pos < len(lines):
            print(term.center(lines[pos] + pos_str))
        else:
            print(term.center("".ljust(width) + pos_str))


if __name__ == "__main__":
    term = Terminal()
    print(term.clear)

    input_loop(term, offline = False, headless = False)

