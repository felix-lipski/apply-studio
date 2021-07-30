from time import sleep
from ui   import print_center_msg, display_lines
from boards.common import check_generated, gen_board, input_pdf_pracujpl


def get_offers(driver):
    offers = []
    for i in range(4):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight*" + str((i + 1) / 4.0) + ")")
    sleep(1)
    fetched_offers       = driver.find_elements_by_class_name("jobs-search-results__list-item")
    for offer_element in fetched_offers:
        obj = {}
        n   = (len(offer_element.find_elements_by_class_name("job-card-list__title")))
        obj["title"]     = str(len(offer_element.find_elements_by_class_name("job-card-list__title")))
        if n > 0:
            obj["title"] = (offer_element.find_element_by_class_name("job-card-list__title").text)
        obj["company"]   = offer_element.find_element_by_class_name("job-card-container__company-name").text
        obj["element"]   = offer_element
        quick_apply = obj["element"].find_element_by_class_name("job-card-list__footer-wrapper").find_elements_by_class_name("job-card-container__apply-method")
        obj["quick"] = len(quick_apply) > 0
        obj["generated"] = check_generated(obj)
        offers.append(obj)
    return offers


def handle_offer(driver, term, offers, selection):
    offer = offers[selection]
    el = offer["element"]
    url = el.find_element_by_tag_name("a").get_attribute('href')
    lines = ["", "", term.black_on_white(term.center(offer["title"])), term.black_on_white(term.center(offer["company"])),]

    if offer["quick"]:
        lines.append(term.blue("Quick Apply!"))
    lines.append("")

    print_center_msg(term, "Loading offer...", term.black_on_yellow)
    driver.get(url)
    
    details = driver.find_element_by_id("job-details")

    for ul in details.find_elements_by_tag_name("ul"):
        for li in ul.find_elements_by_tag_name("li"):
            lines.append(li.get_attribute('innerHTML'))
        lines.append("")

    lines.append("")
    lines.append("")

    display_lines(input_pdf_pracujpl(driver, term, offer), term, lines)
    print_center_msg(term, "Returning...", term.black_on_yellow)
    driver.back()
    return driver


board = gen_board("LinkedIn", "https://www.linkedin.com/jobs/search/?f_E=1%2C2&keywords=React", get_offers, handle_offer)


