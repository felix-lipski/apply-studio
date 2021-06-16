from blessed import Terminal

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import sleep

driver = webdriver.Firefox()
driver.get("http://www.python.org")
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
sleep(20)
driver.close()


term = Terminal()

print(term.home + term.clear + term.move_y(term.height // 2))
print(term.black_on_blue(term.center('press any key to continue.')))
print([1,2,3,"foo"])

with term.cbreak(), term.hidden_cursor():
    inp = term.inkey()

print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))
