import os, sys, time
from platform import system
import argparse

if os.name == "nt":
    from msvcrt import getch
elif os.name == "posix":
    import termios, tty
else:
    sys.exit("Operating system not recognised")

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
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ] \
                + [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # time modified
        case 2:
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ] \
                + [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # name
        case _: # 0 and unrecognised values
            dirs = sorted([x for x in os.listdir() if os.path.isdir(x) and (settings["hidden"] or not x.startswith(".") )], key=lambda s: s.lower()) \
                + sorted([x for x in os.listdir() if os.path.isfile(x) and (settings["hidden"] or not x.startswith(".") )], key=lambda s: s.lower())
    return dirs


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
    to_print = "pyleManager ---- press i for instructions\n\n"
    max_l = os.get_terminal_size().columns # length of terminal
    if len(os.path.abspath(os.getcwd())) > max_l:
        to_print += "... " + os.path.abspath(os.getcwd())[-max_l+5:] + "/\n"
    else:
        to_print += os.path.abspath(os.getcwd()) + "/\n"
    # folders and pointer
    if len(directory()) == 0:
        to_print += "**EMPTY FOLDER**\n"
    else:
        order_update(0)
        index_dir()
        temp = directory()[index]
        l_size = max((len(file_size(x)) for x in directory()))
        l_time = 19
        to_print += " " + "v"*(settings["order"] == 0) + " "*(settings["order"] != 0) + "*NAME*"   
        if settings["dimension"] and True in (os.path.isfile(x) for x in directory()):
            to_print += " "*(max_l - max(l_size,6) - (l_time + 2)*(settings["time_modified"] == True) - 10 + (settings["order"] != 1 )) + "v"*(settings["order"] == 1) + "*SIZE*"
        if settings["time_modified"] and True in (os.path.isfile(x) for x in directory()):
            to_print += " "*(max(l_size - 3,3)*(settings["dimension"] == True) + (max_l - 27)*(settings["dimension"] == False) - 1 - (settings["order"] == 2)) + "v"*(settings["order"] == 2) + "*TIME_M*"
        for x in directory():
            to_print += "\n"
            if x == temp:
                to_print += "+"
            else:
                to_print += " "
            if os.path.isdir(x):
                to_print += "<"
            else:
                to_print += " "
            if len(x) > max_l - 37 + l_size*(settings["dimension"] == 0) + l_time*(settings["time_modified"] == 0):
                name_x = x[:(max_l-39)//2] + " ... " +\
                          x[-(max_l-39)//2 - (l_size+2)*(settings["dimension"] == 0) - (l_time+2)*(settings["time_modified"] == 0):]
            else:
                name_x = x
            to_print += name_x
            if settings["dimension"] and os.path.isfile(x):
                to_print += " "*(max_l - 4 - len(name_x) - max(l_size,6) - (l_time+2)*(settings["time_modified"] == True)) + file_size(x)
            if settings["time_modified"] and os.path.isfile(x):
                time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.lstat(x).st_mtime)))
                to_print += " "*( (max(l_size,6) - len(file_size(x)) + 2 )*(settings["dimension"] == True) + (max_l - 23 - len(name_x))*(settings["dimension"] == False)) + time_stamp
    print(to_print)


# FETCH KEYBOARD INPUT
if os.name == "posix":
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    conv_arrows = {"D":"left", "C":"right", "A":"up", "B":"down"}
    def get_key():
        key_pressed = getch()
        match key_pressed:
            case "\r":
                return "enter"
            case "\x1b":
                if getch() == "[":
                    return conv_arrows[getch()]
            case _:
                return key_pressed
else:
    conv_table = {
        b"q":"q", b"h":"h", b"m":"m", b"i":"i", b"t":"t", b"d":"d", b"e":"e", b"\r":"enter",
        b"\xe0":"arrows"
        }
    conv_arrows = {b"K":"left", b"M":"right", b"H":"up", b"P":"down"}
    def get_key():
        key_pressed = conv_table[getch()]
        if key_pressed != "arrows":
            return key_pressed
        else:
            return conv_arrows[getch()]
        


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
        match get_key():
            # quit
            case "q":
                with open(local_folder + "settings.py","w") as settings_file: 
                    settings_file.write("settings = " + str(settings)) # save config
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
            # enter
            case "enter" if len(directory()) > 0:
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
            # up
            case "up" if len(directory()) > 0:
                index = index - 1
            # down
            case "down" if len(directory()) > 0:
                index = index + 1
            # right
            case "right" if len(directory()) > 0:
                if os.path.isdir(selection):
                    os.chdir(selection)
            # left
            case "left":
                os.chdir("..")
            case _:
                pass
        dir_printer()


if __name__ == "__main__":
    main()
