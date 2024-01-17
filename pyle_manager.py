""" built-in cross-platform modules """
import os
import sys
import time
import argparse
import itertools
from platform import system

if os.name == "posix":
    import termios
    import tty
elif os.name == "nt":
    from msvcrt import getch as getch_encoded
else:
    sys.exit("Operating system not recognised")


# parsing args
parser = argparse.ArgumentParser(prog="pyleManager",
                                 description="file manager written in Python")
parser.add_argument("-p", "--picker",
                    action="store_true",
                    help="use pyleManager as a file selector")
args = parser.parse_args()  # args.picker contains the modality

# immutable settings
PICKER = args.picker
LOCAL_FOLDER = os.path.abspath(os.getcwd())  # save original path

# mutable settings


class Settings:
    """ class containing the global settings """

    def __init__(self) -> None:
        self.size = False
        self.time = False
        self.hidden = False
        self.beep = False
        self.permission = False
        self.order = 0
        self.current_directory = ""
        self.rows_length = os.get_terminal_size().lines
        self.start_line_directory = 0
        self.selection = ""
        self.index = 0

    def change_size(self) -> None:
        """ toggle size """
        self.size = not self.size

    def change_time(self) -> None:
        """ toggle time """
        self.time = not self.time

    def change_hidden(self) -> None:
        """ toggle hidden """
        self.hidden = not self.hidden

    def change_beep(self) -> None:
        """ toggle beep """
        self.beep = not self.beep

    def change_permission(self) -> None:
        """ toggle permission """
        self.permission = not self.permission

    def update_order(self, stay: bool) -> None:
        """ update order, False stay, True move to the next entry """
        old_order = settings.order
        # create a vector with (1,a,b) where a,b are one if dimension and TIME_MODIFIED are enabled
        settings_enabled = (1,
                            settings.size * any(os.path.isfile(x)
                                                for x in directory()),
                            settings.time)
        # search the next 1 and if not found return 0
        settings.order = settings_enabled.index(
            1, settings.order+stay) if 1 in settings_enabled[settings.order+stay:] else 0
        if settings.order != old_order:
            # only update if the previous order was changed
            settings.current_directory = ""

    def update_rows_length(self) -> None:
        """ update the length of the rows in the terminal window """
        self.rows_length = os.get_terminal_size().lines

    def update_selection(self):
        """ update the name of the selected folder """
        if len(directory()) > 0:
            settings.selection = directory()[settings.index]


settings = Settings()


# --------------------------------------------------


def file_size(path: str) -> str:
    """ return file size as a formatted string """
    size = os.lstat(path).st_size
    i = len(str(size)) // 3
    if len(str(size)) % 3 == 0:
        i -= 1
    if i > 3:
        i = 3
    size /= 1000**i
    return f'{size:.2f}{("b", "kb", "mb", "gb")[i]}'


def directory() -> list[str]:
    """ list of folders and files """
    # return the previous value if exists
    if not settings.current_directory:
        directories = os.listdir()
        # order by
        match settings.order:
            # size
            case 1:
                dirs = list(itertools.chain(sorted((x for x in directories
                                                    if os.path.isdir(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda x: os.lstat(x).st_size),
                                            sorted((x for x in directories
                                                    if os.path.isfile(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda x: os.lstat(x).st_size)))
            # time modified
            case 2:
                dirs = list(itertools.chain(sorted((x for x in directories
                                                    if os.path.isdir(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda x: os.lstat(x).st_mtime),
                                            sorted((x for x in directories
                                                    if os.path.isfile(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda x: os.lstat(x).st_mtime)))
            # name
            case _:  # 0 or unrecognised values
                dirs = list(itertools.chain(sorted((x for x in directories
                                                    if os.path.isdir(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda s: s.lower()),
                                            sorted((x for x in directories
                                                    if os.path.isfile(x) and (settings.hidden or not x.startswith("."))),
                                                    key=lambda s: s.lower())))
        settings.current_directory = dirs
    return settings.current_directory


# CLEAN TERMINAL
if os.name == "posix":
    def clear():
        """ clear screen """
        os.system("clear")
elif os.name == "nt":
    def clear():
        """ clear screen """
        os.system("cls")


def dir_printer(position: str = "beginning") -> None:
    """ printing function """

    # first check if I only have to print the index:
    if position == "up":
        settings.index -= 1
        if settings.index >= settings.start_line_directory:
            # print up when we are in the range of visibility
            sys.stdout.write('\033[2A')
            print()
            return  # exit the function

        # else print up one
        settings.start_line_directory -= 1
        position = "beginning"  # return the cursor up

    elif position == "down":
        settings.index += 1
        if settings.index < settings.rows_length - 3 + settings.start_line_directory:
            # print down when we are in the range of visibility
            print()
            return  # exit the function

        # else print down 1
        settings.start_line_directory += 1

    clear()
    # length of columns
    columns_len = os.get_terminal_size().columns
    # path directory
    to_print = [
        "### pyleManager --- press i for instructions ###"[:columns_len], "\n"]
    # name folder
    to_print.append('... ' if len(os.path.abspath(os.getcwd()))
                    > columns_len else '')
    to_print.append(os.path.abspath(os.getcwd())[5-columns_len:])
    if not to_print[-1].endswith(os.sep):
        to_print.append(os.sep)
    to_print.append("\n")
    # folders and pointer
    if len(directory()) == 0:
        to_print.append(" **EMPTY FOLDER**")
        position = None
    else:
        settings.update_order(False)
        l_size = max((len(file_size(x)) for x in directory()))

        # write the description on top
        to_print.append(" v*NAME*" if settings.order == 0 else "  *NAME*")

        columns = []
        if settings.size and any(os.path.isfile(x) for x in directory()):
            columns.append(" |v" if settings.order == 1 else " | ")
            columns.append("*SIZE*")
            columns.append(' '*(l_size-6))
        if settings.time:
            columns.append(" |v" if settings.order == 2 else " | ")
            columns.append("*TIME MODIFIED*")
            columns.append(" "*4)
        if settings.permission:
            columns.append(" | *PERM*")
        columns = "".join(columns)

        to_print.append(" "*(columns_len - len(columns)-8))
        to_print.append(columns)

        if position == "index":
            if len(directory())-1 < settings.index:
                settings.index = len(directory())-1
            if settings.index >= settings.rows_length - 3:
                settings.start_line_directory = settings.index - \
                    (settings.rows_length - 3) + 1

        for x in itertools.islice(directory(), settings.start_line_directory, settings.start_line_directory + settings.rows_length - 3):
            to_print.append("\n <" if os.path.isdir(x) else "\n  ")

            # add extensions
            columns = []
            if settings.size and os.path.isfile(x):
                columns.append(" | ")
                columns.append(file_size(x))
                columns.append(" "*(l_size - len(file_size(x))))
            if settings.time:
                columns.append(" | ")
                columns.append(time.strftime('%Y-%m-%d %H:%M:%S',
                               time.strptime(time.ctime(os.lstat(x).st_mtime))))

            if settings.permission:
                columns.append(" | ")
                columns.append("r " if os.access(x, os.R_OK)
                               else "- ")  # read permission
                columns.append("w " if os.access(x, os.W_OK)
                               else "- ")  # write permission
                columns.append("x " if os.access(x, os.X_OK) else "- ")
            columns = "".join(columns)

            name_x = f'... {x[-(columns_len - 6 - len(columns)):]}' if len(x) > columns_len - 2 - len(columns) else x
            to_print.append(name_x)
            to_print.append(" "*(columns_len-len(name_x)-len(columns) - 2))
            to_print.append(columns)

    print("".join(to_print), end="\r")

    if position == "beginning":
        sys.stdout.write(
            f'\033[{min(len(directory()), settings.rows_length-3)}A')
        print()
    elif position == "index":
        if settings.index < settings.rows_length - 3:
            sys.stdout.write(
                f'\033[{min(len(directory()), settings.rows_length-3) - settings.index}A')
            print()


# FETCH KEYBOARD INPUT
if os.name == "posix":
    def getch() -> str:
        """ read raw terminal input """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    conv_arrows = {"D": "left", "C": "right", "A": "up", "B": "down"}
    def get_key() -> str:
        """ process correct string for keyboard input """
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case "\x1b":
                if getch() == "[":
                    return conv_arrows.get(getch(), None)
            case _:
                return key_pressed

elif os.name == "nt":
    def getch() -> str:
        """ read raw terminal input """
        letter = getch_encoded()
        try:
            return letter.decode('ascii')
        except:
            return letter

    conv_arrows = {"K": "left", "M": "right", "H": "up", "P": "down"}
    def get_key() -> str:
        """ process correct string for keyboard input """
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case b"\xe0":
                return conv_arrows.get(getch(), None)
            case _:
                return key_pressed


def beeper() -> None:
    """ make a beep """
    if settings.beep:
        sys.stdout.write('\033[2A')
        print("\a\n")


def dir_printer_reset(refresh: bool = False, restore_position: str = "beginning") -> None:
    """ print screen after resetting directory attributes """
    if refresh:
        settings.current_directory = ""

    settings.update_rows_length()
    settings.start_line_directory = 0
    if restore_position == "index":
        pass
    elif restore_position == "selection":
        if settings.selection in directory():
            settings.index = directory().index(settings.selection)
        else:
            settings.index = 0
        restore_position = "index"
    else:
        settings.index = 0

    dir_printer(position=restore_position)


def instructions() -> None:
    """ print instructions """
    clear()
    print(f"""INSTRUCTIONS:

the prefix \"<\" means folder

upArrow = up
downArrow = down
rightArrow = open folder
leftArrow = previous folder
q = quit
r = refresh
h = ({'yes' if settings.hidden else 'no'}) toggle hidden files
d = ({'yes' if settings.size else 'no'}) toggle file size
t = ({'yes' if settings.time else 'no'}) toggle time last modified
b = ({'yes' if settings.beep else 'no'}) toggle beep
p = ({'yes' if settings.permission else 'no'}) toggle permission
m = ({("NAME", "SIZE", "TIME MODIFIED")[settings.order]}) change ordering
enter = {'select file' if PICKER else 'open using the default application launcher'}
e = {'--disabled--' if PICKER else 'edit using command-line editor'}

def selection_permission(path):

press any button to continue""", end="")
    get_key()


# --------------------------------------------------


def main(*args: list[str]) -> None:
    """ file manager """

    if args and args[0] in ("-p", "--picker"):
        global PICKER
        PICKER = True

    dir_printer()

    while True:

        settings.update_selection()

        match get_key():
            # up
            case "up":
                if len(directory()) > 0 and settings.index > 0:
                    dir_printer(position="up")
                else:
                    beeper()

            # down
            case "down":
                if len(directory()) > 0 and settings.index < len(directory())-1:
                    dir_printer(position="down")
                else:
                    beeper()

            # right
            case "right":
                if len(directory()) > 0 and os.path.isdir(settings.selection) and os.access(settings.selection, os.R_OK):
                    os.chdir(settings.selection)
                    dir_printer_reset(refresh=True, restore_position="index")
                else:
                    beeper()

            # left
            case "left":
                if os.path.dirname(os.getcwd()) != os.getcwd():
                    os.chdir("..")
                    dir_printer_reset(refresh=True, restore_position="index")
                else:
                    beeper()

            # quit
            case "q":
                clear()
                os.chdir(LOCAL_FOLDER)
                return

            # refresh
            case "r":
                dir_printer_reset(refresh=True, restore_position="selection")

            # toggle hidden
            case "h":
                settings.change_hidden()
                dir_printer_reset(refresh=True, restore_position="selection")

            # size
            case "d":
                settings.change_size()
                dir_printer_reset(restore_position="selection")

            # time
            case "t":
                settings.change_time()
                dir_printer_reset(restore_position="selection")

            # beep
            case "b":
                settings.change_beep()

            # permission
            case "p":
                settings.change_permission()
                dir_printer_reset(restore_position="selection")

            # change order
            case "m":
                settings.update_order(True)
                dir_printer_reset(restore_position="selection")

            # enter
            case "enter":
                if len(directory()) > 0:
                    if PICKER:
                        path = os.path.join(os.getcwd(), settings.selection)
                        clear()
                        os.chdir(LOCAL_FOLDER)
                        return path
                    elif not PICKER:
                        selection_os = settings.selection.replace("\"", "\\\"")
                        match system():
                            case "Linux":
                                os.system(f"xdg-open \"{selection_os}\"")
                            case "Windows":
                                os.system(selection_os)
                            case "Darwin":
                                os.system(f"open \"{selection_os}\"")
                            case _:
                                clear()
                                print(
                                    "system not recognised, press any button to continue")
                                get_key()
                                dir_printer_reset(restore_position="selection")
                else:
                    beeper()

            # command-line editor
            case "e":
                if len(directory()) > 0 and not PICKER:
                    selection_os = settings.selection.replace("\"", "\\\"")
                    match system():
                        case "Linux":
                            os.system(f"$EDITOR \"{selection_os}\"")
                        case "Windows":
                            clear()
                            print(
                                "Windows does not have any built-in command line editor, press any button to continue")
                            get_key()
                            dir_printer_reset(restore_position="selection")
                        case "Darwin":
                            os.system(f"open -e \"{selection_os}\"")
                        case _:
                            clear()
                            print(
                                "system not recognised, press any button to continue")
                            get_key()
                            dir_printer_reset(restore_position="selection")
                else:
                    beeper()

            # instructions
            case "i":
                instructions()
                dir_printer_reset(restore_position="selection")

            case _:
                pass


if __name__ == "__main__":
    main()
