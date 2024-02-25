""" built-in cross-platform modules """
import os
import time
import argparse
from itertools import chain
from platform import system
import threading
import raw_input


# utility functions
def slice_ij(v: list, i: int, j: int):
    """create an iterator for a given array from i to j"""
    # notice that islice does not work this way, but consume the iterable from the beginning
    return (v[k] for k in range(i, min(len(v), j)))


def getkey() -> str:
    """override the getkey method to return always lower case"""
    return raw_input.getkey().lower()


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
        self.print_latent = False
        self.picker = args.picker

    def change_size(self) -> None:
        """toggle size"""
        self.size = not self.size

    def change_time(self) -> None:
        """toggle time"""
        self.time = not self.time

    def change_hidden(self) -> None:
        """toggle hidden"""
        self.hidden = not self.hidden

    def change_beep(self) -> None:
        """toggle beep"""
        self.beep = not self.beep

    def change_permission(self) -> None:
        """toggle permission"""
        self.permission = not self.permission

    def update_order(self, stay: bool) -> None:
        """update order, False stay, True move to the next entry"""
        old_order = self.order
        # create a vector with (1,a,b) where a,b are one if dimension and TIME_MODIFIED are enabled
        settings_enabled = (
            1,
            self.size * any(os.path.isfile(x) for x in directory()),
            self.time,
        )
        # search the next 1 and if not found return 0
        self.order = (
            settings_enabled.index(1, self.order + stay)
            if 1 in settings_enabled[self.order + stay :]
            else 0
        )
        if self.order != old_order:
            # only update if the previous order was changed
            self.current_directory = ""

    def update_terminal_size(self) -> bool:
        """update the size of the temrinal window"""
        if (
            os.get_terminal_size().lines != self.rows_length
            or os.get_terminal_size().columns != self.cols_length
        ):
            self.rows_length = os.get_terminal_size().lines
            self.cols_length = os.get_terminal_size().columns
            return True
        return False

    def update_selection(self) -> None:
        """update the name of the selected folder"""
        if len(directory()) > 0:
            self.selection = directory()[self.index]

    def key_attach(self) -> None:
        """attach key stdin"""
        if os.name == "posix":
            raw_input.keyboard_attach()

    def key_detach(self) -> None:
        """detach key stdin"""
        if os.name == "posix":
            raw_input.keyboard_detach()

    def change_print_latent(self) -> None:
        """change status latent printer"""
        self.print_latent = not self.print_latent


SETTINGS = Settings()

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
    if not SETTINGS.current_directory:
        directories = os.listdir()
        # order by
        match SETTINGS.order:
            # size
            case 1:
                dirs = chain(
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isdir(x)
                            and (SETTINGS.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_size,
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (SETTINGS.hidden or not x.startswith("."))
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
                            and (SETTINGS.hidden or not x.startswith("."))
                        ),
                        key=lambda x: os.lstat(x).st_mtime,
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (SETTINGS.hidden or not x.startswith("."))
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
                            and (SETTINGS.hidden or not x.startswith("."))
                        ),
                        key=lambda s: s.lower(),
                    ),
                    sorted(
                        (
                            x
                            for x in directories
                            if os.path.isfile(x)
                            and (SETTINGS.hidden or not x.startswith("."))
                        ),
                        key=lambda s: s.lower(),
                    ),
                )
        SETTINGS.current_directory = list(dirs)
    return SETTINGS.current_directory


def dir_printer(position: str = "beginning") -> None:
    """printing function"""

    # first check if I only have to print the index:
    if position == "up":
        SETTINGS.index -= 1
        if SETTINGS.index >= SETTINGS.start_line_directory:
            # print up when we are in the range of visibility
            print("\033[2A\n", end="")
            return  # exit the function

        # else print up one
        SETTINGS.start_line_directory -= 1
        position = "beginning"  # return the cursor up

    elif position == "down":
        SETTINGS.index += 1
        if SETTINGS.index < SETTINGS.rows_length - 3 + SETTINGS.start_line_directory:
            # print down when we are in the range of visibility
            print()
            return  # exit the function

        # else print down 1
        SETTINGS.start_line_directory += 1

    raw_input.clear()
    # path directory
    to_print = [
        "### pyleManager --- press i for instructions ###"[: SETTINGS.cols_length],
        "\n",
    ]
    # name folder
    to_print.append(
        "... " if len(os.path.abspath(os.getcwd())) > SETTINGS.cols_length else ""
    )
    to_print.append(os.path.abspath(os.getcwd())[5 - SETTINGS.cols_length :])
    if not to_print[-1].endswith(os.sep):
        to_print.append(os.sep)
    to_print.append("\n")
    # folders and pointer
    if len(directory()) == 0:
        to_print.append(" **EMPTY FOLDER**")
        position = None
    else:
        SETTINGS.update_order(False)
        l_size = max((len(file_size(x)) for x in directory()))

        # write the description on top
        to_print.append(" v*NAME*" if SETTINGS.order == 0 else "  *NAME*")

        columns = []
        columns_count = 0
        if SETTINGS.size and any(os.path.isfile(x) for x in directory()):
            columns.append(" |v" if SETTINGS.order == 1 else " | ")
            columns.append("*SIZE*")
            columns.append(" " * (l_size - 6))
            columns_count += 3 + l_size
        if SETTINGS.time:
            columns.append(" |v" if SETTINGS.order == 2 else " | ")
            columns.append("*TIME MODIFIED*")
            columns.append(" " * 4)
            columns_count += 22
        if SETTINGS.permission:
            columns.append(" | *PERM*")
            columns_count += 9

        to_print.append(" " * (SETTINGS.cols_length - columns_count - 8))
        to_print.extend(columns)

        if position == "index":
            if len(directory()) - 1 < SETTINGS.index:
                SETTINGS.index = len(directory()) - 1
            if SETTINGS.index >= SETTINGS.rows_length - 3:
                SETTINGS.start_line_directory = (
                    SETTINGS.index - (SETTINGS.rows_length - 3) + 1
                )

        for x in slice_ij(
            directory(),
            SETTINGS.start_line_directory,
            SETTINGS.start_line_directory + SETTINGS.rows_length - 3,
        ):
            to_print.append("\n <" if os.path.isdir(x) else "\n  ")

            # add extensions
            columns = []
            columns_count = 0
            if SETTINGS.size and os.path.isfile(x):
                columns.append(" | ")
                columns.append(file_size(x))
                columns.append(" " * (l_size - len(file_size(x))))
                columns_count += 3 + l_size
            if SETTINGS.time:
                columns.append(" | ")
                columns.append(
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.strptime(time.ctime(os.lstat(x).st_mtime)),
                    )
                )
                columns_count += 22

            if SETTINGS.permission:
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
                f"... {x[-(SETTINGS.cols_length - 6 - columns_count):]
                            }"
                if len(x) > SETTINGS.cols_length - 2 - columns_count
                else x
            )
            to_print.append(name_x)
            to_print.append(
                " " * (SETTINGS.cols_length - len(name_x) - columns_count - 2)
            )
            to_print.extend(columns)

    print(*to_print, sep="", end="\r")

    if position == "beginning":
        print(f"\033[{min(len(directory()), SETTINGS.rows_length-3)}A")
    elif position == "index":
        if SETTINGS.index < SETTINGS.rows_length - 3:
            print(
                f"\033[{min(len(directory()), SETTINGS.rows_length-3) - SETTINGS.index}A"
            )


def beeper() -> None:
    """make a beep"""
    if SETTINGS.beep:
        print("\a", end="\r")


def dir_printer_reset(
    refresh: bool = False, restore_position: str = "beginning"
) -> None:
    """print screen after resetting directory attributes"""
    if refresh:
        SETTINGS.current_directory = ""

    SETTINGS.update_terminal_size()
    SETTINGS.start_line_directory = 0
    if restore_position == "index":
        pass
    elif restore_position == "selection":
        if SETTINGS.selection in directory():
            SETTINGS.index = directory().index(SETTINGS.selection)
        else:
            SETTINGS.index = 0
        restore_position = "index"
    else:
        SETTINGS.index = 0

    if os.name == "posix":
        SETTINGS.key_detach()

    dir_printer(position=restore_position)

    if os.name == "posix":
        SETTINGS.key_attach()


def latent_printer() -> None:
    """threaded function that reprints screen if change in terminal"""
    while SETTINGS.print_latent:
        time.sleep(0.1)
        if SETTINGS.update_terminal_size():
            dir_printer_reset(refresh=False, restore_position="index")


def pre_quit(latent_printer_daemon: threading.Thread) -> None:
    """running to execute before quitting"""
    raw_input.clear()
    os.chdir(LOCAL_FOLDER)
    if SETTINGS.print_latent:
        SETTINGS.change_print_latent()
        latent_printer_daemon.join()


def instructions() -> None:
    """print instructions"""
    raw_input.clear()
    print(
        f"""INSTRUCTIONS:

the prefix \"<\" means folder

upArrow = up
downArrow = down
rightArrow = open folder
leftArrow = previous folder
q = quit
r = refresh
h = ({'yes' if SETTINGS.hidden else 'no'}) toggle hidden files
d = ({'yes' if SETTINGS.size else 'no'}) toggle file size
t = ({'yes' if SETTINGS.time else 'no'}) toggle time last modified
b = ({'yes' if SETTINGS.beep else 'no'}) toggle beep
p = ({'yes' if SETTINGS.permission else 'no'}) toggle permission
l = ({'yes' if SETTINGS.print_latent else 'no'}) toggle automatic refresh on terminal resize
m = ({("NAME", "SIZE", "TIME MODIFIED")[SETTINGS.order]}) change ordering
enter = {'select file' if SETTINGS.picker else 'open using the default application launcher'}
e = {'--disabled--' if SETTINGS.picker else 'edit using command-line editor'}

def selection_permission(path):

press any button to continue""",
        end="",
    )
    getkey()


# --------------------------------------------------


def main(*args: list[str]) -> None:
    """file manager"""

    if args and args[0] in ("-p", "--picker"):
        SETTINGS.picker = True

    dir_printer_reset(refresh=True, restore_position="beginning")

    # mock process
    latent_printer_daemon = threading.Thread(target=lambda: None, daemon=True)
    latent_printer_daemon.start()

    while True:
        SETTINGS.update_selection()

        match getkey():
            # up
            case "up":
                if len(directory()) > 0 and SETTINGS.index > 0:
                    dir_printer(position="up")
                else:
                    beeper()

            # down
            case "down":
                if len(directory()) > 0 and SETTINGS.index < len(directory()) - 1:
                    dir_printer(position="down")
                else:
                    beeper()

            # right
            case "right":
                if (
                    len(directory()) > 0
                    and os.path.isdir(SETTINGS.selection)
                    and os.access(SETTINGS.selection, os.R_OK)
                ):
                    os.chdir(SETTINGS.selection)
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
                SETTINGS.change_hidden()
                dir_printer_reset(refresh=True, restore_position="selection")

            # size
            case "d":
                SETTINGS.change_size()
                dir_printer_reset(restore_position="selection")

            # time
            case "t":
                SETTINGS.change_time()
                dir_printer_reset(restore_position="selection")

            # beep
            case "b":
                SETTINGS.change_beep()

            # permission
            case "p":
                SETTINGS.change_permission()
                dir_printer_reset(restore_position="selection")

            # terminal resize
            case "l":
                SETTINGS.change_print_latent()
                latent_printer_daemon.join()
                if SETTINGS.print_latent:
                    latent_printer_daemon = threading.Thread(
                        target=latent_printer, daemon=True
                    )
                    latent_printer_daemon.start()

            # change order
            case "m":
                SETTINGS.update_order(True)
                dir_printer_reset(restore_position="selection")

            # enter
            case "enter":
                if len(directory()) > 0:
                    if SETTINGS.picker:
                        path = os.path.join(os.getcwd(), SETTINGS.selection)
                        pre_quit(latent_printer_daemon)
                        return path
                    elif not SETTINGS.picker:
                        selection_os = SETTINGS.selection.replace('"', '\\"')
                        match system():
                            case "Linux":
                                os.system(f'xdg-open "{selection_os}"')
                            case "Windows":
                                os.system(selection_os)
                            case "Darwin":
                                os.system(f'open "{selection_os}"')
                            case _:
                                raw_input.clear()
                                print(
                                    "system not recognised, press any button to continue"
                                )
                                getkey()
                                dir_printer_reset(restore_position="selection")
                else:
                    beeper()

            # command-line editor
            case "e":
                if len(directory()) > 0 and not SETTINGS.picker:
                    selection_os = SETTINGS.selection.replace('"', '\\"')
                    match system():
                        case "Linux":
                            os.system(f'$EDITOR "{selection_os}"')
                        case "Windows":
                            raw_input.clear()
                            print(
                                "Windows does not have any built-in command line editor, press any button to continue"
                            )
                            getkey()
                            dir_printer_reset(restore_position="selection")
                        case "Darwin":
                            os.system(f'open -e "{selection_os}"')
                        case _:
                            raw_input.clear()
                            print("system not recognised, press any button to continue")
                            getkey()
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
