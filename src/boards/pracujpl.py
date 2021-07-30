from pdf  import gen_pdf
from ui   import print_center_msg, display_lines, select_option
from boards.common import check_generated, gen_board


def get_offers(driver):
    offers = []
    fetched_offers = driver.find_elements_by_class_name("offer-details__text")
    for offer_element in fetched_offers:
        obj = {}
        obj["title"] = (offer_element.find_element_by_tag_name("h2").text)
        obj["company"] = (offer_element.find_element_by_class_name("offer-company__name").text)
        obj["element"] = offer_element.find_element_by_xpath("../../..")
        quick_apply = obj["element"].find_element_by_class_name("offer__info").find_elements_by_class_name("offer-labels__item--one-click-apply")
        obj["quick"] = len(quick_apply) > 0
        obj["generated"] = check_generated(obj)
        offers.append(obj)
    return offers


def handle_offer(driver, term, offers, selection):
    offer = offers[selection]
    el = offer["element"]
    regions = el.find_elements_by_class_name("offer-regions__port") + el.find_elements_by_class_name("offer-regions")
    regions = regions[0].find_elements_by_class_name("offer-regions__label")
    regions = list(map(
        lambda x: {"name": x.get_attribute('innerHTML'), "element": x}
        , regions))
    url = ""
    if len(regions) > 0:
        url = select_option(driver, term, regions)
    else:
        url = el.find_element_by_class_name("offer__info").find_element_by_class_name("offer-details__title-link").get_attribute('href')
    if url:
        print_center_msg(term, "Loading offer...", term.black_on_yellow)
        lines = ["", "", term.black_on_white(term.center(offer["title"])), term.black_on_white(term.center(offer["company"])),]
        if offer["quick"]:
            lines.append(term.blue("Quick Apply!"))
        lines.append("")
        driver.get(url)
        panels = driver.find_elements_by_class_name("OfferView1PIsMp")
        for panel in panels:
            lists = panel.find_elements_by_tag_name("ul")
            if len(lists) == 0:
                for p in panel.find_elements_by_tag_name("p"):
                    lines.append(p.text)
            for lst in lists:
                ps = lst.find_elements_by_tag_name("p")
                for p in ps:
                    lines.append(p.text)
                if len(ps) == 0:
                    for li in lst.find_elements_by_tag_name("li"):
                        lines.append(li.text)
                lines.append("".ljust(term.width))
            lines.append("".ljust(term.width, "─"))
        lines.append("")
        lines.append("")

        display_lines(input_pdf(driver, term, offer), term, lines)
        print_center_msg(term, "Returning...", term.black_on_yellow)
        driver.back()
    return driver


def input_pdf(driver, term, offer):
    def function():
        driver.get(driver.find_element_by_class_name("OfferView1sEL6l").get_attribute('href'))
        pdf_file_path = gen_pdf(term, offer)
        file_input_el = driver.find_element_by_class_name("file__input")
        file_input_el.send_keys(pdf_file_path)
        send_button = driver.find_element_by_class_name("send-section__trigger")
    return function


board = gen_board("pracuj.pl", "https://www.pracuj.pl/praca/react;kw?rd=30&et=17", get_offers, handle_offer)


