from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from blessed import Terminal

from browse import load_browser
from graphics import print_center_msg

def handle_offer(driver, url):
    driver.get(url)
    print(term.clear)
    val = ""
    while val.lower() != "q":
        print("test")
        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                pass
        elif val:
            if val == "j":
                pass
            if val == "k":
                pass
    driver.back()
    return driver



def get_offers(driver, company = "pracuj.pl"):
    offers = []
    if company == "pracuj.pl":
        fetched_offers = driver.find_elements_by_class_name("offer-details__text")
        for offer_element in fetched_offers:
            obj = {}
            obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
            obj["company"] = (offer_element.find_element_by_class_name("offer-company__name").text)
            obj["element"] = offer_element.find_element_by_xpath("../../..")
            offers.append(obj)
    return offers

def print_debug(term, msg):
    print(term.home + term.white_on_red(term.bold(msg)))

def select_region(driver, term, regions):
    val = ""
    selection = 0
    while val.lower() != "q":
        print(term.home)
        for i, region in enumerate(regions):
            region_text = ((region["name"]).ljust(30))
            if i == selection:
                region_text = term.black_on_white(region_text)
            print(region_text, i)
        print(selection)

            
        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                url = regions[selection]["element"].get_attribute('href')
                return url
        elif val:
            if val == "j":
                selection = (selection + 1) % (len(regions))
            if val == "k":
                selection = (selection - 1) % (len(regions))
    return ""

def input_loop(term, offline = False, headless = False):
    driver = 0
    offers = []
    debug_msg = ""
    if offline == False:
        driver = load_browser(term, headless = headless)
        offers = get_offers(driver)
    else:
        offers = [
                {"company": "first company", "title": "first job"},
                {"company": "second company", "title": "second job"},
                {"company": "third company", "title": "third company"},
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
            print_debug(term, debug_msg)
            val = term.inkey()
            if not val:
                pass
              # print("It sure is quiet in here ...")
            elif val.is_sequence:
                # print("got sequence: {0}.".format((str(val), val.name, val.code)))
                if val.name == "KEY_ENTER":
                    # print("enter")
                    el = offers[selection]["element"]
                    regions = el.find_elements_by_class_name("offer-regions__port") + el.find_elements_by_class_name("offer-regions")
                    regions = regions[0].find_elements_by_class_name("offer-regions__label")
                    regions = list(map(
                        lambda x: {"name": x.get_attribute('innerHTML'), "element": x}
                        , regions))
                    url = ""
                    if len(regions) > 0:
                        # debug_msg = regions[0]["name"]
                        url = select_region(driver, term, regions)
                    else:
                        # debug_msg = str(len(regions))
                        url = el.find_element_by_class_name("offer__info").find_element_by_class_name("offer-details__title-link").get_attribute('href')
                    driver = handle_offer(driver, url, "https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
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

