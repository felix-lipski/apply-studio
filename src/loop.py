from browse import load_browser
from ui     import print_center_msg, print_debug, print_board_name, print_offers
from pdf    import gen_pdf
from boards import Board


def input_loop(term, offline = False, headless = False):
    # board = Board.PRACUJPL
    # board = Board.NOFLUFFJOBS
    # board = Board.JUSTJOINIT
    board = Board.LINKEDIN

    driver    = 0
    offers    = []
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
    selection    = 0
    scroll       = 0
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
                    driver = board.value["offer_handler"](driver, term, offers, selection)
                    offers = board.value["offers_getter"](driver)
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


