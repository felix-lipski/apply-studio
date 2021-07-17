from browse import load_browser
from graphics import print_center_msg, print_debug, print_board_name
from pdf import gen_pdf
from boards import Board


def handle_offer(driver, term, url, offer):
    scroll = 0
    lines = ["", "", term.black_on_white(term.center(offer["title"])), term.black_on_white(term.center(offer["company"])),]
    if offer["quick"]:
        lines.append(term.blue("Quick Apply!"))
    lines.append("")
    print_center_msg(term, "Loading offer...", term.black_on_yellow)
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

    print(term.clear)
    val = ""
    while val.lower() != "q":
        for i in range(term.height):
            if i < len(lines):
                print(lines[i + scroll])
        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                driver.get(driver.find_element_by_class_name("OfferView1sEL6l").get_attribute('href'))
                pdf_file_path = gen_pdf(offer["company"])
                file_input_el = driver.find_element_by_class_name("file__input")
                file_input_el.send_keys(pdf_file_path)
                send_button = driver.find_element_by_class_name("send-section__trigger")
        elif val:
            if val == "j":
                scroll = min(scroll + 1, len(lines) - term.height) 
            if val == "k":
                scroll = max(scroll - 1, 0)
    print_center_msg(term, "Returning...", term.black_on_yellow)
    driver.back()
    return driver


def select_region(driver, term, regions):
    val = ""
    selection = 0
    while val.lower() != "q":
        print(term.home + term.move_y(term.height//2 - len(regions)//2))
        print(term.center("┌" + "".ljust(30, "─") + "┐"))
        for i, region in enumerate(regions):
            region_text = ((region["name"]).ljust(30))
            if i == selection:
                region_text = term.black_on_white(region_text)
            print(term.center("│" + region_text + "│"))
        print(term.center("└" + "".ljust(30, "─") + "┘"))
        # print(selection)

        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                url = regions[selection]["element"].get_attribute('href')
                return url
        elif val:
            if val == "j":
                selection = (selection + 1) % (len(regions))
            if val == "k":
                selection = (selection - 1) % (len(regions))
    return False



def input_loop(term, offline = False, headless = False):
    # board = Board.PRACUJPL
    board = Board.NOFLUFFJOBS
    # board = Board.JUSTJOINIT
    driver = 0
    offers = []
    debug_msg = ""
    if offline == False:
        driver = load_browser(term, headless = headless, board = board)
        offers = board.value["offers_getter"](driver)
    else:
        offers = [
            {"company": "first company", "title": "first job"},
            {"company": "second company", "title": "second job"},
            {"company": "third company", "title": "third company"},
            {"company": "third to last company", "title": "third to last job"},
            {"company": "second to last company", "title": "second to last job"},
            {"company": "last company", "title": "last job"},
        ]
    selection = 0
    scroll = 0
    offer_height = 3
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        val = ""
        while val.lower() != "q":
            print_offers(term, offers, selection, scroll)
            print_board_name(term, board.value["name"])
            print_debug(term, debug_msg)
            val = term.inkey()
            if not val:
                pass
            elif val.is_sequence:
                # print("got sequence: {0}.".format((str(val), val.name, val.code)))
                if val.name == "KEY_ENTER":
                    el = offers[selection]["element"]
                    regions = el.find_elements_by_class_name("offer-regions__port") + el.find_elements_by_class_name("offer-regions")
                    regions = regions[0].find_elements_by_class_name("offer-regions__label")
                    regions = list(map(
                        lambda x: {"name": x.get_attribute('innerHTML'), "element": x}
                        , regions))
                    url = ""
                    if len(regions) > 0:
                        # debug_msg = regions[0]["name"]
                        url = select_region(driver, term, regions)
                    else:
                        # debug_msg = str(len(regions))
                        url = el.find_element_by_class_name("offer__info").find_element_by_class_name("offer-details__title-link").get_attribute('href')
                    if url:
                        driver = handle_offer(driver, term, url, offers[selection])
                        offers = get_offers(driver)
            elif val:
                if val == "j":
                    selection = min(selection + 1, max(len(offers) - 1, 0))
                    if (selection*offer_height) >= term.height - 8:
                        scroll = min(scroll+offer_height, (len(offers) + 2) * offer_height - term.height)
                    
                if val == "k":
                    selection = max(selection - 1, 0)
                    if (selection*offer_height) - scroll <= 4:
                        scroll = max(scroll-offer_height, 0)
                if val == "r":
                    driver.get("https://www.pracuj.pl/praca/react;kw?rd=30&et=17")
        print(term.clear)
        print_center_msg(term, 'bye!')
    return 0



def print_offers(term, offers, selection, scroll):
    width = 60
    lines = []
    for i, offer in enumerate(offers):
        quick_apply = "".ljust(12)
        if offer["quick"]:
            quick_apply = term.white_on_blue("Quick Apply!")
        title = (" " + offer["title"]).ljust(width - 12)[:(width - 12)] + quick_apply
        company = ((offer["company"]).ljust(width))[:width]
        if i == selection:
            title = (term.black_on_white(title))
            company = (term.black_on_white(company))
        lines.append((title))
        lines.append((company))
        lines.append("".ljust(width, "─"))

    print(term.home)
    for i in range(term.height - 6):
        pos = i + (scroll)
        pos_str = ""
        # pos_str = str(pos)
        if scroll <= pos < term.height - 6 + scroll and pos < len(lines):
            print(term.center(lines[pos] + pos_str))
        else:
            print(term.center("".ljust(width) + pos_str))

