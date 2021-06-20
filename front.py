from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from blessed import Terminal



def load_browser(headless = True):
    fireFoxOptions = webdriver.FirefoxOptions()
    if headless:
        fireFoxOptions.set_headless()
    browser = webdriver.Firefox(firefox_options=fireFoxOptions)
    browser.maximize_window()
    
    class EventListeners(AbstractEventListener):
        def after_click(self, element, driver):
            print("after_click %s" %element)
    
    driver = EventFiringWebDriver(browser, EventListeners())
    
    driver.get("https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
    print("loaded")
    return driver



def input_loop(offline = False):
    driver = 0
    offers = []
    if offline == False:
        driver = load_browser()
        fetched_offers = driver.find_elements_by_class_name("offer-details__text")
        for offer_element in fetched_offers:
            obj = {}
            obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
            obj["company"] = (offer_element.find_element_by_class_name("offer-company__name").text)
            obj["element"] = offer_element
            offers.append(obj)
    else:
        # Test Offers
        offers = [
                {"company": "foo", "title": "janitor"},
                {"company": "bar", "title": "monitor"},
                {"company": "baz", "title": "clerk"},
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
                {"company": "barr22", "title": "monitor"},
                {"company": "baze22", "title": "clerk"},
                {"company": "quiz22", "title": "man"},
                ]
    selection = 0
    scroll = 0
    rerender = "offers"
    with term.cbreak(), term.hidden_cursor():
        val = ""
        while val.lower() != "q":
            if rerender:
                rerender = False
                print(term.clear)
                print_offers(term, offers, selection, scroll)
            val = term.inkey()
            if not val:
                pass
              # print("It sure is quiet in here ...")
            elif val.is_sequence:
                print("got sequence: {0}.".format((str(val), val.name, val.code)))
            elif val:
                if val == "j":
                    selection = min(selection + 1, max(len(offers) - 1, 0))
                    if (selection*2) >= term.height - 4:
                        scroll = min(scroll+2, len(offers) * 2)
                    rerender = "offers"
                    
                if val == "k":
                    selection = max(selection - 1, 0)
                    if (selection*2) - scroll <= 4:
                        scroll = max(scroll-2, 2)
                    rerender = "offers"
                if val == "r":
                    driver.get("https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
        print(f'bye!{term.normal}')



def print_offers(term, offers, selection, scroll):
    width = 60
    print(term.home)
    for i, offer in enumerate(offers):
        if (i*2) - scroll < (term.height - 2) and (i*2) >= scroll:
            title = term.bold(("  " + offer["title"]).ljust(width))
            company = (offer["company"]).ljust(width)
            if i == selection:
                title = (term.black_on_green(title))
                company = (term.black_on_green(company))
            print(term.center(title))
            print(term.center(company))



term = Terminal()
print(term.clear)



input_loop(offline = False)



