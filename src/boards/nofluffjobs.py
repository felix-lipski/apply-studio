from boards.common import check_generated, gen_board


def get_offers(driver):
    offers = []
    fetched_offers = driver.find_elements_by_class_name("posting-list-item")
    for offer_element in fetched_offers:
        obj = {}
        obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
        obj["company"] = (offer_element.find_element_by_class_name("company").text)
        obj["element"] = offer_element
        obj["quick"] = False
        obj["generated"] = check_generated(obj)
        offers.append(obj)
    return offers


board = gen_board("No Fluff Jobs", "https://nofluffjobs.com/pl/jobs/react?criteria=seniority%3Dtrainee,junior", get_offers, None)


