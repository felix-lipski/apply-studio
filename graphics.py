def print_center_msg(term, msg, color_func):
    print(term.clear + term.move_y(term.height // 2) + 
            term.center(
                color_func(
                    " " + msg + " "
                    )
                )
            )
