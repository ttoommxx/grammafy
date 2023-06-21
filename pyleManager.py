import os, sys, termios, tty, time
from platform import system
import argparse

parser = argparse.ArgumentParser(prog="pyleManager", description="file manager written in Python")
parser.add_argument("-p", "--picker", action="store_true", help="use pyleManager as a file selector")
args = parser.parse_args() # args.picker contains the modality
picker = args.picker


local_folder = os.path.abspath(os.getcwd()) + "/" # save original path
from settings import * # just import local settings
index = 0 # dummy index


# INSTRUCTION PRINTER
def instructions():
    print(f"""INSTRUCTIONS:
          
    prefix < means folder

    leftArrow = previous folder
    rightArrow = open folder
    upArrow = up
    downArrow = down
    q = quit
    h = toggle hidden files
    d = toggle file size
    t = toggle time last modified
    m = change ordering
    enter = {'select file' if picker else 'open using the default application launcher'}
    e = {'--disabled--' if picker else 'edit using command-line editor'}

press any button to continue""")


# UPDATE INDEX DIRECTORY
def index_dir():
    global index
    if len(directory()) > 0: # first of all update index
        index %= len(directory())
    else:
        index = 0


# RETURN FILE SIZE AS A STRING
def file_size(path):
    size = os.lstat(path).st_size
    i = 0
    while size > 999:
        size /= 1000
        i += 1
    return f"{size:.2f}" + ("b","kb","mb","gb")[i]


# UPDATE ORDER, 0 stay 1 next
def order_update(j):
    global settings
    vec = (1, int(settings["dimension"])*(True in (os.path.isfile(x) for x in directory())),
           int(settings["time_modified"])*(True in (os.path.isfile(x) for x in directory())))
    settings["order"] = vec.index(1,settings["order"]+j) if 1 in vec[settings["order"]+j:] else 0


# LIST OF FOLDERS AND FILES
def directory():
    # order by
    match settings["order"]:
        # size
        case 1:
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
            files = [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # time modified
        case 2:
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
            files = [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # name
        case _: # 0 and unrecognised values
            dirs = sorted([x for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )], key=lambda s: s.lower())
            files = sorted([x for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )], key=lambda s: s.lower())
    return dirs + files


# CLEAN TERMINAL
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# PRINTING FUNCTION
def dir_printer():
    clear()
    # path directory
    to_print = "pyleManager ---- press i for instructions\n\n" + os.path.abspath(os.getcwd()) + "/\n"
    # folders and pointer
    if len(directory()) == 0:
        to_print += "**EMPTY FOLDER**\n"
    else:
        order_update(0)
        index_dir()
        temp = directory()[index]
        l_size = max((len(file_size(x)) for x in directory()))
        l_time = 19
        max_l = os.get_terminal_size().columns # length of terminal
        to_print += " " + "v"*(settings["order"] == 0) + " "*(settings["order"] != 0) + "*NAME*"   
        if settings["dimension"] and True in (os.path.isfile(x) for x in directory()):
            to_print += " "*(max_l - max(l_size,6) - (l_time + 2)*(settings["time_modified"] == True) - 10 + (settings["order"] != 1 )) + "v"*(settings["order"] == 1) + "*SIZE*"
        if settings["time_modified"] and True in (os.path.isfile(x) for x in directory()):
            to_print += " "*(max(l_size - 3,3)*(settings["dimension"] == True) + (max_l - 27)*(settings["dimension"] == False) - 1 - (settings["order"] == 2)) + "v"*(settings["order"] == 2) + "*TIME_M*"
        to_print += "\n"
        for x in directory():
            if x == temp:
                to_print += "-"
            else:
                to_print += " "
            if os.path.isdir(x):
                to_print += "<"
            else:
                to_print += " "
            to_print += x
            if settings["dimension"] and os.path.isfile(x):
                to_print += " "*(max_l - 4 - len(x) - max(l_size,6) - (l_time+2)*(settings["time_modified"] == True)) + file_size(x)
            if settings["time_modified"] and os.path.isfile(x):
                time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.lstat(x).st_mtime)))
                to_print += " "*( (max(l_size,6) - len(file_size(x)) + 2 )*(settings["dimension"] == True) + (max_l - 23 - len(x))*(settings["dimension"] == False)) + time_stamp
            to_print += "\n"
    print(to_print)


# FETCH KEYBOARD INPUT
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# FILE MANAGER
def main(*args):
    if args and args[0] in ["-p", "--picker"]:
        global picker
        picker = True
    global index
    global settings
    dir_printer()
    while True:
        if len(directory()) > 0:
            selection = directory()[index] # + file name if any
        match getch():
            # quit
            case "q":
                open(local_folder + "settings.py","w").write("settings = " + str(settings)) # save config
                clear()
                os.chdir(local_folder)
                return
            # toggle hidden
            case "h":
                temp = directory()[index]
                settings["hidden"] = not settings["hidden"]
                if len(directory()) > 0:
                    if temp in directory(): # update index
                        index = directory().index(temp)
                    else:
                        index = 0
            # change order
            case "m":
                if len(directory()) > 0:
                    temp = directory()[index]
                order_update(1)
                if len(directory()) > 0:
                    index = directory().index(temp)
            # instructions
            case "i":
                clear()
                instructions()
                getch()
            case "t":
                settings["time_modified"] = not settings["time_modified"]
            # size
            case "d":
                settings["dimension"] = not settings["dimension"]
            # command-line editor
            case "e" if len(directory()) > 0 and not picker:
                match system():
                    case "Linux":
                        os.system("$EDITOR " + selection)
                    case "Windows":
                        clear()
                        print("Windows does not have any built-in command line editor, press any button to continue")
                        getch()
                    case "Darwin":
                        os.system("open -e " + selection)
                    case _:
                        clear()
                        print("system not recognised, press any button to continue")
                        getch()
            case "\r" if len(directory()) > 0:
                if picker:
                    path = os.getcwd() + "/" + selection
                    if  os.path.isdir(selection):
                        path += "/"
                    os.chdir(local_folder)
                    return path
                elif not picker:
                    match system():
                        case "Linux":
                            os.system("xdg-open " + selection)
                        case "Windows":
                            os.system(selection)
                        case "Darwin":
                            os.system("open " + selection)
                        case _:
                            clear()
                            print("system not recognised, press any button to continue")
                            getch()
            case "\x1b":
                if getch() == "[":
                    match getch():
                        # up
                        case "A" if len(directory()) > 0:
                            index = index - 1
                        # down
                        case "B" if len(directory()) > 0:
                            index = index + 1
                        # right
                        case "C" if len(directory()) > 0:
                            if os.path.isdir(selection):
                                os.chdir(selection)
                        # left
                        case "D":
                            os.chdir("..")
                        case _:
                            pass
            case _:
                pass
        dir_printer()


if __name__ == "__main__":
    main()
