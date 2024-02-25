""" cross platofrm module to handle raw input from terminal """
import os
import sys
from typing import NoReturn

# posix utils
if os.name == "posix":
    import termios
    import tty

    class Vars:
        """Posix terminal variables"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        conv_arrows = {"D": "left", "C": "right", "A": "up", "B": "down"}

    VARS = Vars()

    def keyboard_attach() -> NoReturn:
        """attach keyboard input"""
        tty.setraw(VARS.fd)

    def keyboard_detach() -> NoReturn:
        """detach keyboard input"""
        termios.tcsetattr(VARS.fd, termios.TCSADRAIN, VARS.old_settings)

    def clear() -> NoReturn:
        """clear screen"""
        os.system("clear")

    def getch() -> str:
        """read raw terminal input"""

        try:
            keyboard_attach()
            ch = sys.stdin.read(1)
        finally:
            keyboard_detach()
        return ch

    def getkey() -> str:
        """process correct string for keyboard input"""
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case "\t":
                return "tab"
            case "\x1b":
                if getch() == "[":
                    return VARS.conv_arrows.get(getch(), None)
            case "\x7f":
                return "backspace"
            case _:
                return key_pressed

elif os.name == "nt":
    from msvcrt import getch as getch_encoded

    class Vars:
        """Windows terminal variables"""

        conv_arrows = {"K": "left", "M": "right", "H": "up", "P": "down"}

    VARS = Vars()

    def clear() -> NoReturn:
        """clear screen"""
        os.system("cls")

    def getch() -> str:
        """read raw terminal input"""
        letter = getch_encoded()
        try:
            return letter.decode("ascii")
        except SyntaxError:
            return letter

    def getkey() -> str:
        """process correct string for keyboard input"""
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case "\t":
                return "tab"
            case b"\xe0":
                return VARS.conv_arrows.get(getch(), None)
            case b"\x08":
                return "backspace"
            case _:
                return key_pressed

else:
    sys.exit("Operating system not recognised")
