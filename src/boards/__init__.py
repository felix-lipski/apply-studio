from enum import Enum

import boards.pracujpl
import boards.linkedin
import boards.nofluffjobs
import boards.justjoinit

class Board(Enum):
    PRACUJPL    = pracujpl.board
    NOFLUFFJOBS = nofluffjobs.board
    JUSTJOINIT  = justjoinit.board
    LINKEDIN    = linkedin.board
