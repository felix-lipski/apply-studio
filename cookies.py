import pickle

def save_cookies(driver):
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

def load_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
