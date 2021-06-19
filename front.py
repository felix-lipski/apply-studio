from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from pynput import mouse, keyboard

headless = False
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


offers = []

def handle_input(key):
    try:
        char = key.char
        global driver
        if char == "r":
            driver.get("https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
        elif char == "e":
            global offers
            offers = driver.find_elements_by_class_name("offer-details__text")
            for el in offers:
                print(el.find_element_by_tag_name("h2").text)
                print(el.find_element_by_class_name("offer-company__name").text, "\n")
        elif char == "n":
            driver.find_element_by_class_name("pagination_trigger").click()

    except AttributeError:
        print('special key {0} pressed'.format(
            key))




listener = keyboard.Listener(on_press=handle_input)
listener.start()

def on_click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked')
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

time.sleep(10)
