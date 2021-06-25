from blessed import Terminal
import pickle

from browse import load_browser
from graphics import print_center_msg

term = Terminal()

print_center_msg(term, "yes", term.black_on_green)


browser = load_browser(term, headless = False)

def save_cookies(driver):
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

def load_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def print_cookies(term, browser):
    print(term.clear)
    cookies = browser.get_cookies()
    for cookie in cookies:
        print(cookie)

val = ""
while val.lower() != "q":
    val = term.inkey()
    if val == "c":
        print_cookies(term, browser)
    if val == "s":
        save_cookies(browser)
    if val == "l":
        load_cookies(browser)
