from time import sleep
from boards.common import check_generated, gen_board, input_pdf_pracujpl


def get_offers(driver):
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


board = gen_board("Just Join IT", "https://justjoin.it/all/all/junior?q=React@category", get_offers, None)


