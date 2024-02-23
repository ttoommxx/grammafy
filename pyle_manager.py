""" built-in cross-platform modules """
import os
import sys
import time
import argparse
from itertools import chain
from platform import system
import threading
from typing import Any, Generator, NoReturn


# utility functions
def slice_ij(v: list[Any], i: int, j: int) -> Generator:
    """create an iterator for a given array from i to j"""
    # notice that islice does not work this way, but consume the iterable from the beginning
    return (v[k] for k in range(i, min(len(v), j)))


if os.name == "posix":
    import termios
    import tty
elif os.name == "nt":
    from msvcrt import getch as getch_encoded
else:
    sys.exit("Operating system not recognised")


# parsing args
parser = argparse.ArgumentParser(
    prog="pyleManager", description="file manager written in Python"
)
parser.add_argument(
    "-p", "--picker", action="store_true", help="use pyleManager as a file selector"
)
args = parser.parse_args()  # args.picker contains the modality


# immutable settings
LOCAL_FOLDER = os.path.abspath(os.getcwd())  # save original path


# mutable settings
class Settings:
    """class containing the global settings"""

    def __init__(self):
        self.size = False
        self.time = False
        self.hidden = False
        self.beep = False
        self.permission = False
        self.order = 0
        self.current_directory = ""
        self.rows_length = os.get_terminal_size().lines
        self.cols_length = os.get_terminal_size().columns
        self.start_line_directory = 0
        self.selection = ""
        self.index = 0
        fd = sys.stdin.fileno()
        self.terminal_status = (fd, termios.tcgetattr(fd))
        self.print_latent = False
        self.picker = args.picker

    def change_size(self) -> NoReturn:
        """toggle size"""
        self.size = not self.size

    def change_time(self) -> NoReturn:
        """toggle time"""
        self.time = not self.time

    def change_hidden(self) -> NoReturn:
        """toggle hidden"""
        self.hidden = not self.hidden

    def change_beep(self) -> NoReturn:
        """toggle beep"""
        self.beep = not self.beep

    def change_permission(self) -> NoReturn:
        """toggle permission"""
        self.permission = not self.permission

    def update_order(self, stay: bool) -> NoReturn:
        """update order, False stay, True move to the next entry"""
        old_order = settings.order
        # create a vector with (1,a,b) where a,b are one if dimension and TIME_MODIFIED are enabled
        settings_enabled = (
            1,
            settings.size * any(os.path.isfile(x) for x in directory()),
            settings.time,
        )
        # search the next 1 and if not found return 0
        settings.order = (
            settings_enabled.index(1, settings.order + stay)
            if 1 in settings_enabled[settings.order + stay :]
            else 0
        )
        if settings.order != old_order:
            # only update if the previous order was changed
            settings.current_directory = ""

    def update_terminal_size(self) -> bool:
        """update the size of the temrinal window"""
        if (
            os.get_terminal_size().lines != settings.rows_length
            or os.get_terminal_size().columns != settings.cols_length
        ):
            self.rows_length = os.get_terminal_size().lines
            self.cols_length = os.get_terminal_size().columns
            return True
        return False

    def update_selection(self) -> NoReturn:
        """update the name of the selected folder"""
        if len(directory()) > 0:
            settings.selection = directory()[settings.index]

    def key_attach(self) -> NoReturn:
        """attach key stdin"""
        fd, _ = settings.terminal_status
        tty.setraw(fd)

    def key_detach(self) -> NoReturn:
        """detach key stdin"""
        fd, old_settings = settings.terminal_status
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def change_print_latent(self) -> NoReturn:
        """change status latent printer"""
        self.print_latent = not self.print_latent


settings = Settings()

# --------------------------------------------------


def file_size(path: str) -> str:
    """return file size as a formatted string"""
    size = os.lstat(path).st_size
    i = len(str(size)) // 3
    if len(str(size)) % 3 == 0:
        i -= 1
    if i > 3:
        i = 3
    size /= 1000**i
    return f'{size:.2f}{("b", "kb", "mb", "gb")[i]}'


def directory() -> list[str]:
    """list of folders and files"""
    # return the previous value if exists
    if not settings.current_directory:
        directories = os.listdir()
        # order by
        match settings.order:
            # size
            case 1:
                dirs = chain(
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isdir(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_size,
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_size,
                    ),
                )
            # time modified
            case 2:
                dirs = chain(
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isdir(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_mtime,
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_mtime,
                    ),
                )
            # name
            case _:  # 0 or unrecognised values
                dirs = chain(
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isdir(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda s: s.lower(),
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (settings.hidden or not x.startswith("."))
                        ),
                        key=lambda s: s.lower(),
                    ),
                )
        settings.current_directory = list(dirs)
    return settings.current_directory


# CLEAN TERMINAL
if os.name == "posix":

    def clear():
        """clear screen"""
        os.system("clear")
elif os.name == "nt":

    def clear():
        """clear screen"""
        os.system("cls")


def dir_printer(position: str = "beginning") -> NoReturn:
    """printing function"""

    # first check if I only have to print the index:
    if position == "up":
        settings.index -= 1
        if settings.index >= settings.start_line_directory:
            # print up when we are in the range of visibility
            print("\033[2A\n", end="")
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
    # path directory
    to_print = [
        "### pyleManager --- press i for instructions ###"[: settings.cols_length],
        "\n",
    ]
    # name folder
    to_print.append(
        "... " if len(os.path.abspath(os.getcwd())) > settings.cols_length else ""
    )
    to_print.append(os.path.abspath(os.getcwd())[5 - settings.cols_length :])
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
        columns_count = 0
        if settings.size and any(os.path.isfile(x) for x in directory()):
            columns.append(" |v" if settings.order == 1 else " | ")
            columns.append("*SIZE*")
            columns.append(" " * (l_size - 6))
            columns_count += 3 + l_size
        if settings.time:
            columns.append(" |v" if settings.order == 2 else " | ")
            columns.append("*TIME MODIFIED*")
            columns.append(" " * 4)
            columns_count += 22
        if settings.permission:
            columns.append(" | *PERM*")
            columns_count += 9

        to_print.append(" " * (settings.cols_length - columns_count - 8))
        to_print.extend(columns)

        if position == "index":
            if len(directory()) - 1 < settings.index:
                settings.index = len(directory()) - 1
            if settings.index >= settings.rows_length - 3:
                settings.start_line_directory = (
                    settings.index - (settings.rows_length - 3) + 1
                )

        for x in slice_ij(
            directory(),
            settings.start_line_directory,
            settings.start_line_directory + settings.rows_length - 3,
        ):
            to_print.append("\n <" if os.path.isdir(x) else "\n  ")

            # add extensions
            columns = []
            columns_count = 0
            if settings.size and os.path.isfile(x):
                columns.append(" | ")
                columns.append(file_size(x))
                columns.append(" " * (l_size - len(file_size(x))))
                columns_count += 3 + l_size
            if settings.time:
                columns.append(" | ")
                columns.append(
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.strptime(time.ctime(os.lstat(x).st_mtime)),
                    )
                )
                columns_count += 22

            if settings.permission:
                columns.append(" | ")
                columns.append(
                    "r " if os.access(x, os.R_OK) else "- "
                )  # read permission
                columns.append(
                    "w " if os.access(x, os.W_OK) else "- "
                )  # write permission
                columns.append("x " if os.access(x, os.X_OK) else "- ")
                columns_count += 9

            name_x = (
                f"... {x[-(settings.cols_length - 6 - columns_count):]
                            }"
                if len(x) > settings.cols_length - 2 - columns_count
                else x
            )
            to_print.append(name_x)
            to_print.append(
                " " * (settings.cols_length - len(name_x) - columns_count - 2)
            )
            to_print.extend(columns)

    print(*to_print, sep="", end="\r")

    if position == "beginning":
        print(f"\033[{min(len(directory()), settings.rows_length-3)}A")
    elif position == "index":
        if settings.index < settings.rows_length - 3:
            print(
                f"\033[{min(len(directory()), settings.rows_length-3) - settings.index}A"
            )


# FETCH KEYBOARD INPUT
if os.name == "posix":

    def getch() -> str:
        """read raw terminal input"""
        try:
            settings.key_attach()
            ch = sys.stdin.read(1)
        finally:
            settings.key_detach()
        return ch

    conv_arrows = {"D": "left", "C": "right", "A": "up", "B": "down"}

    def get_key() -> str:
        """process correct string for keyboard input"""
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
        """read raw terminal input"""
        letter = getch_encoded()
        try:
            return letter.decode("ascii")
        except:
            return letter

    conv_arrows = {"K": "left", "M": "right", "H": "up", "P": "down"}

    def get_key() -> str:
        """process correct string for keyboard input"""
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case b"\xe0":
                return conv_arrows.get(getch(), None)
            case _:
                return key_pressed


def beeper() -> NoReturn:
    """make a beep"""
    if settings.beep:
        print("\a", end="\r")


def dir_printer_reset(
    refresh: bool = False, restore_position: str = "beginning"
) -> NoReturn:
    """print screen after resetting directory attributes"""
    if refresh:
        settings.current_directory = ""

    settings.update_terminal_size()
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

    if os.name == "posix":
        settings.key_detach()

    dir_printer(position=restore_position)

    if os.name == "posix":
        settings.key_attach()


def latent_printer() -> NoReturn:
    """threaded function that reprints screen if change in terminal"""
    while settings.print_latent:
        time.sleep(0.1)
        if settings.update_terminal_size():
            dir_printer_reset(refresh=False, restore_position="index")


def pre_quit(latent_printer_daemon: threading.Thread) -> NoReturn:
    """running to execute before quitting"""
    clear()
    os.chdir(LOCAL_FOLDER)
    if settings.print_latent:
        settings.change_print_latent()
        latent_printer_daemon.join()


def instructions() -> NoReturn:
    """print instructions"""
    clear()
    print(
        f"""INSTRUCTIONS:

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
l = ({'yes' if settings.print_latent else 'no'}) toggle automatic refresh on terminal resize
m = ({("NAME", "SIZE", "TIME MODIFIED")[settings.order]}) change ordering
enter = {'select file' if settings.picker else 'open using the default application launcher'}
e = {'--disabled--' if settings.picker else 'edit using command-line editor'}

def selection_permission(path):

press any button to continue""",
        end="",
    )
    get_key()


# --------------------------------------------------


def main(*args: list[str]) -> NoReturn:
    """file manager"""

    if args and args[0] in ("-p", "--picker"):
        settings.picker = True

    dir_printer_reset(refresh=True, restore_position="beginning")

    # mock process
    latent_printer_daemon = threading.Thread(target=lambda: None, daemon=True)
    latent_printer_daemon.start()

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
                if len(directory()) > 0 and settings.index < len(directory()) - 1:
                    dir_printer(position="down")
                else:
                    beeper()

            # right
            case "right":
                if (
                    len(directory()) > 0
                    and os.path.isdir(settings.selection)
                    and os.access(settings.selection, os.R_OK)
                ):
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
                pre_quit(latent_printer_daemon)
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

            # terminal resize
            case "l":
                settings.change_print_latent()
                latent_printer_daemon.join()
                if settings.print_latent:
                    latent_printer_daemon = threading.Thread(
                        target=latent_printer, daemon=True
                    )
                    latent_printer_daemon.start()

            # change order
            case "m":
                settings.update_order(True)
                dir_printer_reset(restore_position="selection")

            # enter
            case "enter":
                if len(directory()) > 0:
                    if settings.picker:
                        path = os.path.join(os.getcwd(), settings.selection)
                        pre_quit(latent_printer_daemon)
                        return path
                    elif not settings.picker:
                        selection_os = settings.selection.replace('"', '\\"')
                        match system():
                            case "Linux":
                                os.system(f'xdg-open "{selection_os}"')
                            case "Windows":
                                os.system(selection_os)
                            case "Darwin":
                                os.system(f'open "{selection_os}"')
                            case _:
                                clear()
                                print(
                                    "system not recognised, press any button to continue"
                                )
                                get_key()
                                dir_printer_reset(restore_position="selection")
                else:
                    beeper()

            # command-line editor
            case "e":
                if len(directory()) > 0 and not settings.picker:
                    selection_os = settings.selection.replace('"', '\\"')
                    match system():
                        case "Linux":
                            os.system(f'$EDITOR "{selection_os}"')
                        case "Windows":
                            clear()
                            print(
                                "Windows does not have any built-in command line editor, press any button to continue"
                            )
                            get_key()
                            dir_printer_reset(restore_position="selection")
                        case "Darwin":
                            os.system(f'open -e "{selection_os}"')
                        case _:
                            clear()
                            print("system not recognised, press any button to continue")
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
