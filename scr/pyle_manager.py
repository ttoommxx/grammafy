"""built-in cross-platform modules"""

import os
import time
import argparse
import ctypes
from itertools import chain
from platform import system
import unicurses as uc  # type: ignore


# mutable settings
class Settings:
    """class containing the global settings"""

    def __init__(self) -> None:
        # immutables
        self.file_size_vars = ("b", "kb", "mb", "gb")

        # mutable
        self.size = False
        self.time = False
        self.hidden = False
        self.beep = False
        self.permission = False
        self.order = 0

        # reset at each execution
        self.current_directory: list[str]
        self.start_line_directory: int
        self.selection: str
        self.index: int

        # init variables
        self.picker: bool
        self.local_folder: str

    def init(self, picker: bool) -> None:
        """initialise settings to the current session"""

        # reset at each different execution
        self.current_directory = []
        self.start_line_directory = 0
        self.selection = ""
        self.index = 0

        # init variables
        self.picker = picker
        self.local_folder = os.path.abspath(os.getcwd())
        uc.cbreak()
        uc.noecho()
        uc.keypad(uc.stdscr, True)
        uc.curs_set(0)
        uc.leaveok(uc.stdscr, True)

    @property
    def rows(self) -> int:
        """return rows length"""

        return uc.getmaxy(uc.stdscr)

    @property
    def cols(self) -> int:
        """return columns length"""

        return uc.getmaxx(uc.stdscr)

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
            self.size * any(os.path.isfile(x) for x in _directory()),
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
            self.current_directory = []

    def update_selection(self) -> None:
        """update the name of the selected folder"""

        if len(_directory()) > 0:
            self.selection = _directory()[self.index]

    def quit(self) -> None:
        """quitting routines"""

        os.chdir(self.local_folder)
        uc.endwin()


SETTINGS = Settings()

# --------------------------------------------------


def _file_size(path: str) -> str:
    """return file size as a formatted string"""
    size = os.lstat(path).st_size
    i = len(str(size)) // 3
    if len(str(size)) % 3 == 0:
        i -= 1
    if i > 3:
        i = 3
    display_size = size / 1000**i
    return f"{display_size:.2f}{SETTINGS.file_size_vars[i]}"


def _directory() -> list[str]:
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


def _print_line(line_num: int, k: int, l_size: int) -> None:
    x = _directory()[k]
    if os.path.isdir(x):
        uc.mvaddch(3 + line_num, 1, "<")

    # add extensions
    columns_count = 0
    if SETTINGS.permission and SETTINGS.cols - columns_count - 9 + 1 >= 8:
        columns_count += 9
        uc.mvaddstr(
            3 + line_num,
            SETTINGS.cols - columns_count + 1,
            "| "
            + ("r " if os.access(x, os.R_OK) else "- ")
            + ("w " if os.access(x, os.W_OK) else "- ")
            + ("x" if os.access(x, os.X_OK) else "-"),
        )
    if SETTINGS.time and SETTINGS.cols - columns_count - 22 + 1 >= 8:
        columns_count += 22
        uc.mvaddstr(
            3 + line_num,
            SETTINGS.cols - columns_count + 1,
            "| "
            + time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.strptime(time.ctime(os.lstat(x).st_mtime)),
            ),
        )
    if (
        SETTINGS.size
        and os.path.isfile(x)
        and SETTINGS.cols - columns_count - 3 - l_size + 1 >= 8
    ):
        columns_count += 3 + l_size
        uc.mvaddstr(
            3 + line_num,
            SETTINGS.cols - columns_count + 1,
            "| " + _file_size(x),
        )
    if len(x) > SETTINGS.cols - 2 - columns_count:
        name_x = "... " + x[-(SETTINGS.cols - 6 - columns_count) :]
    else:
        name_x = x
    uc.mvaddwstr(3 + line_num, 2, name_x)


def _dir_printer(refresh: bool = False, position: str = "beginning") -> None:
    """printing function"""

    # check positions and fix index accordingly
    if refresh:
        SETTINGS.current_directory = []
        SETTINGS.start_line_directory = 0

    # init vars
    l_size = max((len(_file_size(x)) for x in _directory())) if _directory() else 0

    if position == "beginning":
        SETTINGS.start_line_directory = 0
        SETTINGS.index = 0

    elif position == "selection":
        if SETTINGS.selection in _directory():
            SETTINGS.index = _directory().index(SETTINGS.selection)
        else:
            SETTINGS.index = 0
        # correct in case we go out of monitor
        SETTINGS.start_line_directory = max(0, 4 + SETTINGS.index - SETTINGS.rows)
        position = "index"

    elif position == "up":
        SETTINGS.index -= 1
        if SETTINGS.index >= SETTINGS.start_line_directory:
            uc.mvaddch(3 + SETTINGS.index - SETTINGS.start_line_directory + 1, 0, " ")
            uc.mvaddch(3 + SETTINGS.index - SETTINGS.start_line_directory, 0, "-")

        else:
            # else print up one
            SETTINGS.start_line_directory -= 1

            uc.move(3, 0)
            uc.insertln()

            _print_line(0, SETTINGS.start_line_directory, l_size)
            uc.mvaddch(4, 0, " ")
            uc.mvaddch(3, 0, "-")
        return

    elif position == "down":
        SETTINGS.index += 1
        if SETTINGS.index < SETTINGS.rows - 3 + SETTINGS.start_line_directory:
            uc.mvaddch(3 + SETTINGS.index - SETTINGS.start_line_directory - 1, 0, " ")
            uc.mvaddch(3 + SETTINGS.index - SETTINGS.start_line_directory, 0, "-")

        else:
            # else print down 1

            uc.move(3, 0)
            uc.deleteln()

            max_line = min(
                len(_directory()),
                SETTINGS.start_line_directory + SETTINGS.rows - 3,
            )

            SETTINGS.start_line_directory += 1

            _print_line(SETTINGS.rows - 4, max_line, l_size)
            uc.mvaddch(SETTINGS.rows - 2, 0, " ")
            uc.mvaddch(SETTINGS.rows - 1, 0, "-")
        return

    max_line = min(
        len(_directory()),
        SETTINGS.start_line_directory + SETTINGS.rows - 3,
    )

    # print on screen
    uc.clear()

    # path directory
    uc.mvaddstr(0, 0, "# pyleManager --- press i for instructions #"[: SETTINGS.cols])
    # name folder
    name_folder = (
        "... " if len(os.path.abspath(os.getcwd())) > SETTINGS.cols else ""
    ) + os.path.abspath(os.getcwd())[5 - SETTINGS.cols :]
    if not name_folder.endswith(os.sep):
        name_folder += os.sep
    uc.mvaddwstr(1, 0, name_folder)

    # folders and pointer
    if len(_directory()) == 0:
        uc.mvaddstr(2, 1, "**EMPTY FOLDER**")
        position = ""
        return

    SETTINGS.update_order(False)

    # write the description on top
    columns_count = 0
    uc.mvaddstr(2, 1, "v*NAME*" if SETTINGS.order == 0 else " *NAME*")
    if SETTINGS.permission and SETTINGS.cols - columns_count - 9 + 1 >= 8:
        columns_count += 9
        uc.mvaddstr(2, SETTINGS.cols - columns_count + 1, ("| *PERM*"))
    if SETTINGS.time and SETTINGS.cols - columns_count - 22 + 1 >= 8:
        columns_count += 22
        uc.mvaddstr(
            2,
            SETTINGS.cols - columns_count + 1,
            ("|v" if SETTINGS.order == 2 else "| ") + "*TIME MODIFIED*",
        )
    if (
        SETTINGS.size
        and any(os.path.isfile(x) for x in _directory())
        and SETTINGS.cols - columns_count - 3 - l_size + 1 >= 8
    ):
        columns_count += 3 + l_size
        uc.mvaddstr(
            2,
            SETTINGS.cols - columns_count + 1,
            ("|v" if SETTINGS.order == 1 else "| ") + "*SIZE*",
        )

    if position == "index":
        if len(_directory()) - 1 < SETTINGS.index:
            SETTINGS.index = len(_directory()) - 1
        if SETTINGS.index >= SETTINGS.rows - 3:
            SETTINGS.start_line_directory = SETTINGS.index - (SETTINGS.rows - 3) + 1

    for line_num, k in enumerate(
        range(
            SETTINGS.start_line_directory,
            max_line,
        )
    ):
        _print_line(line_num, k, l_size)

    if position == "beginning":
        uc.mvaddch(3, 0, "-")
    elif position == "index":
        uc.mvaddch(SETTINGS.index - SETTINGS.start_line_directory + 3, 0, "-")


def _beeper() -> None:
    """make a beep"""
    if SETTINGS.beep:
        uc.beep()


def _instructions() -> None:
    """print instructions"""

    uc.clear()

    lines = [
        "INSTRUCTIONS:",
        "",
        'the prefix "<" means folder',
        "",
        "upqArrow = up",
        "downArrow = down",
        "r = refresh",
        f"h = ({'yes' if SETTINGS.hidden else 'no'}) toggle hidden files",
        f"d = ({'yes' if SETTINGS.size else 'no'}) toggle file size",
        f"t = ({'yes' if SETTINGS.time else 'no'}) toggle time last modified",
        f"b = ({'yes' if SETTINGS.beep else 'no'}) toggle beep",
        f"p = ({'yes' if SETTINGS.permission else 'no'}) toggle permission"
        f"m = ({('NAME', 'SIZE', 'TIME MODIFIED')[SETTINGS.order]}) change ordering"
        f"enter = {'select file' if SETTINGS.picker else 'open using the default application launcher'}",
        f"e = {'--disabled--' if SETTINGS.picker else 'edit using command-line editor'}"
        "",
        " -press q to quit-",
    ]
    nlines = len(lines)
    start_line = 0
    end_line = min(SETTINGS.rows - 1, nlines - 1)

    for i in range(start_line, end_line + 1):
        uc.mvaddstr(i, 0, lines[i])

    while True:
        button = uc.getkey()
        if button == "q":
            break
        elif button == "KEY_UP":
            if start_line > 0:
                start_line -= 1
                end_line -= 1
                uc.move(0, 0)
                uc.insertln()
                uc.mvaddstr(0, 0, lines[start_line])
        elif button == "KEY_DOWN":
            if end_line < nlines - 1:
                start_line += 1
                end_line += 1
                uc.move(0, 0)
                uc.deleteln()
                uc.mvaddstr(SETTINGS.rows - 1, 0, lines[end_line])


# --------------------------------------------------


def _file_manager(stdscr: ctypes.c_void_p, picker: bool) -> str:
    """file manager, wrapped by unicurses"""

    SETTINGS.init(picker)

    while SETTINGS.rows < 4 or SETTINGS.cols < 8:
        uc.mvaddstr(0, 0, "RESIZE")
        uc.getkey()

    _dir_printer(refresh=True, position="beginning")

    output = ""

    while True:
        SETTINGS.update_selection()

        match uc.getkey():
            # up
            case "KEY_UP":
                if len(_directory()) > 0 and SETTINGS.index > 0:
                    _dir_printer(position="up")
                else:
                    _beeper()

            # down
            case "KEY_DOWN":
                if len(_directory()) > 0 and SETTINGS.index < len(_directory()) - 1:
                    _dir_printer(position="down")
                else:
                    _beeper()

            # right
            case "KEY_RIGHT":
                if (
                    len(_directory()) > 0
                    and os.path.isdir(SETTINGS.selection)
                    and os.access(SETTINGS.selection, os.R_OK)
                ):
                    os.chdir(SETTINGS.selection)
                    _dir_printer(refresh=True, position="beginning")
                else:
                    _beeper()

            # left
            case "KEY_LEFT":
                if os.path.dirname(os.getcwd()) != os.getcwd():
                    os.chdir("..")
                    _dir_printer(refresh=True, position="beginning")
                else:
                    _beeper()

            # quit
            case "q":
                break

            # refresh
            case "r":
                _dir_printer(refresh=True, position="selection")

            # toggle hidden
            case "h":
                SETTINGS.change_hidden()
                _dir_printer(refresh=True, position="selection")

            # size
            case "d":
                SETTINGS.change_size()
                _dir_printer(position="selection")

            # time
            case "t":
                SETTINGS.change_time()
                _dir_printer(position="selection")

            # beep
            case "b":
                SETTINGS.change_beep()

            # permission
            case "p":
                SETTINGS.change_permission()
                _dir_printer(position="selection")

            # change order
            case "m":
                SETTINGS.update_order(True)
                _dir_printer(position="selection")

            # enter
            case "^J":
                if len(_directory()) > 0:
                    if SETTINGS.picker:
                        path = os.path.join(os.getcwd(), SETTINGS.selection)
                        output = path
                        break

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
                                uc.clear()
                                uc.mvaddstr(
                                    0,
                                    0,
                                    "System not recognised, press any button to continue",
                                )
                                uc.getkey()
                                _dir_printer(position="selection")
                else:
                    _beeper()

            # command-line editor
            case "e":
                if len(_directory()) > 0 and not SETTINGS.picker:
                    selection_os = SETTINGS.selection.replace('"', '\\"')
                    match system():
                        case "Linux":
                            os.system(f'$EDITOR "{selection_os}"')
                        case "Windows":
                            uc.clear()
                            uc.mvaddstr(
                                0,
                                0,
                                "Windows does not have any built-in command line editor, press any button to continue",
                            )
                            uc.getkey()
                            _dir_printer(position="selection")
                        case "Darwin":
                            os.system(f'open -e "{selection_os}"')
                        case _:
                            uc.clear()
                            uc.mvaddstr(
                                0,
                                0,
                                "System not recognised, press any button to continue",
                            )
                            uc.getkey()
                            _dir_printer(position="selection")
                else:
                    _beeper()

            # instructions
            case "i":
                _instructions()
                _dir_printer(position="selection")

            case "KEY_RESIZE":
                if SETTINGS.rows < 4 or SETTINGS.cols < 8:
                    uc.clear()
                    uc.mvaddstr(0, 0, "RESIZE")
                else:
                    _dir_printer(position="selection")

            case _:
                pass

    SETTINGS.quit()

    return output


def file_manager(picker: bool = False) -> str:
    """file manager"""

    return uc.wrapper(_file_manager, picker)


if __name__ == "__main__":
    # parsing args
    parser = argparse.ArgumentParser(
        prog="pyleManager", description="file manager written in Python"
    )
    parser.add_argument(
        "-p", "--picker", action="store_true", help="use pyleManager as a file selector"
    )
    args = parser.parse_args()  # args.picker contains the modality

    file_manager(args.picker)
