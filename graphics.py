def print_center_msg(term, msg, color_func):
    print(term.move_y(term.height // 2) + 
            term.center(
                color_func(
                    " " + msg + " "
                    )
                )
            )



def print_debug(term, msg):
    print(term.home + term.white_on_red(term.bold(msg)))



def print_loading(term):
    text = " Loading... "
    print(term.home + term.move_xy(term.width//2 - len(text)//2, term.height//2) + term.white_on_yellow(text))
