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
