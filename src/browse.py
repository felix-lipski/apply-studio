from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from graphics import print_center_msg
from boards import Board


def load_browser(term, headless = True, board = Board.NOFLUFFJOBS):
    print(term.clear)
    print_center_msg(term, "Starting browser...", term.black_on_yellow)

    browser = "Chrome"

    if browser == "Firefox":
        fireFoxOptions = webdriver.FirefoxOptions()
        if headless:
            fireFoxOptions.add_argument("--headless")
        browser = webdriver.Firefox(options=fireFoxOptions)
        browser.maximize_window()
    elif browser == "Chrome":
        chrome_options = webdriver.chrome.options.Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--user-data-dir=data/chrome")
        browser = webdriver.Chrome(options=chrome_options)
    
    print_center_msg(term, "Loading page...", term.black_on_yellow)

    class EventListeners(AbstractEventListener):
        def after_click(self, element, driver):
            print("after_click %s" %element)
    
    driver = EventFiringWebDriver(browser, EventListeners())
    
    driver.get(board.value["url"])

    print_center_msg(term, "Loaded!", term.black_on_blue)
    return driver
