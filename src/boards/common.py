from csv  import reader
from pdf  import gen_pdf


def check_generated(offer):
    with open('data/pdf/generated.csv', newline='') as csvfile:
        spamreader = reader(csvfile)
        if len(list(filter(lambda x: x[0] == offer["company"] and x[1] == offer["title"], spamreader))) > 0:
            return True
    return False


def input_pdf_pracujpl(driver, term, offer):
    def function():
        driver.get(driver.find_element_by_class_name("OfferView1sEL6l").get_attribute('href'))
        pdf_file_path = gen_pdf(term, offer)
        file_input_el = driver.find_element_by_class_name("file__input")
        file_input_el.send_keys(pdf_file_path)
        send_button = driver.find_element_by_class_name("send-section__trigger")
    return function


def gen_board(name, url, offers_getter, offer_handler):
    return { "name": name, "url": url, "offers_getter": offers_getter, "offer_handler": offer_handler }


