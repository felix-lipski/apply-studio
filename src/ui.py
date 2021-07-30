def print_center_msg(term, msg, color_func = None):
    color_func = term.black_on_blue if not color_func else color_func
    print(
            term.home + 
            term.move_y(term.height//2) + 
            term.center(color_func( " " + msg + " "))
    )


def print_debug(term, msg):
    print(
            term.home + 
            term.white_on_red(term.bold(msg))
    )


def print_board_name(term, board_name):
    print(
            term.home + 
            term.black_on_white(term.center(board_name))
    )


def get_text(driver, x):
    driver.execute_script("return arguments[0].textContent", x)


def split_lines(txt, l):
    return [txt[i:i+l] for i in range(0, len(txt), l)]


def display_lines(input_pdf, term, lines):
    print(term.clear)
    scroll = 0
    val = ""
    while val.lower() != "q":
        for i in range(term.height):
            if (i + scroll + 1) < len(lines) and i + scroll > 0:
                print(lines[i + scroll])
            else:
                print(term.center(str(scroll)))
        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                input_pdf()
        elif val:
            if val == "j":
                scroll = min(scroll + 1, term.height - len(lines)) 
            if val == "k":
                scroll = max(scroll - 1, 0)


def select_option(driver, term, options):
    val = ""
    selection = 0
    while val.lower() != "q":
        print(
                term.home + 
                term.move_y(term.height//2 - len(options)//2) +
                term.center("┌" + "".ljust(30, "─") + "┐")
        )
        for i, region in enumerate(options):
            region_text = ((region["name"]).ljust(30))
            if i == selection:
                region_text = term.black_on_white(region_text)
            print(term.center("│" + region_text + "│"))
        print(term.center("└" + "".ljust(30, "─") + "┘"))

        val = term.inkey()
        if not val:
            pass
        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                url = options[selection]["element"].get_attribute('href')
                return url
        elif val:
            if val == "j":
                selection = (selection + 1) % (len(options))
            if val == "k":
                selection = (selection - 1) % (len(options))
    return False


def print_offers(term, offers, selection, scroll):
    width = 60
    lines = []
    for i, offer in enumerate(offers):
        quick_apply = "".ljust(12)
        generated = "".ljust(9)
        if offer["quick"]:
            quick_apply = term.white_on_blue("Quick Apply!")
        if offer["generated"]:
            generated = term.white_on_green("Generated")
        title = (" " + offer["title"]).ljust(width - 12)[:(width - 12)] + quick_apply
        company =   (offer["company"]).ljust(width - 9 )[:(width - 9 )] + generated
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

