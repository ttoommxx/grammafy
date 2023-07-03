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
index = 0 # dummy index
dimension = False 
time_modified = False
hidden = False
order = 0


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
    global order
    vec = (1, int(dimension)*(True in (os.path.isfile(x) for x in directory())),
           int(time_modified)*(True in (os.path.isfile(x) for x in directory())))
    order = vec.index(1,order+j) if 1 in vec[order+j:] else 0


# LIST OF FOLDERS AND FILES
def directory():
    # order by
    match order:
        # size
        case 1:
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isdir(x) and (hidden or not x.startswith(".") )}.items(), key=lambda x:x[1]) ] \
                + [x[0] for x in sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isfile(x) and (hidden or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # time modified
        case 2:
            dirs = [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isdir(x) and (hidden or not x.startswith(".") )}.items(), key=lambda x:x[1]) ] \
                + [x[0] for x in sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isfile(x) and (hidden or not x.startswith(".") )}.items(), key=lambda x:x[1]) ]
        # name
        case _: # 0 and unrecognised values
            dirs = sorted([x for x in os.listdir() if os.path.isdir(x) and (hidden or not x.startswith(".") )], key=lambda s: s.lower()) \
                + sorted([x for x in os.listdir() if os.path.isfile(x) and (hidden or not x.startswith(".") )], key=lambda s: s.lower())
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
    to_print = "pyleManager --- press i for instructions\n\n"
    max_l = os.get_terminal_size().columns # length of terminal
    # name folder
    to_print += f"{'... ' if  len(os.path.abspath(os.getcwd())) > max_l else ''}{os.path.abspath(os.getcwd())[-max_l+5:]}/\n"
    # folders and pointer
    if len(directory()) == 0:
        to_print += "**EMPTY FOLDER**"
    else:
        order_update(0)
        index_dir()
        current_selection = directory()[index]
        l_size = max((len(file_size(x)) for x in directory()))
        l_time = 19
    
        to_print += " " + f"{'v' if order == 0 else ' '}*NAME*"
        temp = ""
        if dimension and True in (os.path.isfile(x) for x in directory()):
            temp += f" |{'v' if order == 1 else ' '}*SIZE*" + " "*(l_size-6)
        if time_modified and True in (os.path.isfile(x) for x in directory()):
            temp += f" |{'v' if order == 2 else ' '}*TIME_M*" + " "*11

        to_print += " "*(max_l - len(temp)-8) + temp

        for x in directory():
            to_print += "\n" + f"{'+' if x == current_selection else ' '}" + f"{'<' if os.path.isdir(x) else ' '}"
            temp = ""
            if dimension and os.path.isfile(x):
                temp += " | " + file_size(x) + " "*(l_size - len(file_size(x)))
            if time_modified and os.path.isfile(x):
                temp += " | " + time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.lstat(x).st_mtime)))
            
            if len(x) > max_l - 6 - (l_size+3)*(dimension == True) - (l_time+3)*(time_modified == True):
                name_x = f"... {x[-(max_l - 6 - (l_size+3)*(dimension == True) - (l_time+3)*(time_modified == True)):]}"
            else:
                name_x = x
            to_print += name_x + " "*(max_l-len(name_x)-len(temp) - 2) + temp
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
    global index, dimension, time_modified, hidden
    dir_printer()
    while True:
        if len(directory()) > 0:
            selection = directory()[index] # + file name if any
        match get_key():
            # quit
            case "q":
                clear()
                os.chdir(local_folder)
                return
            # toggle hidden
            case "h":
                temp = directory()[index]
                hidden = not hidden
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
                time_modified = not time_modified
            # size
            case "d":
                dimension = not dimension
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
