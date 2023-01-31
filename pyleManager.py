import os, sys, termios, tty

local_folder = os.path.abspath(os.getcwd()) + '/' # save original path
index = 0 # dummy index
hidden = False # toggle hidden
dimension = False # toggle file_size
# instructions = 'INSTRUCTIONS:\n\n  leftArrow = previous folder\n  rightArrow = open folder\select file\n  upArrow = up\n  downArrow = down\n  q = quit\n  h = toggle hidden files\n  d = toggle file size\n  prefix ■ means folder\n\npress any button to continue'

instructions = '''INSTRUCTIONS:
  leftArrow = previous folder
  rightArrow = open folder\select file
  upArrow = up
  downArrow = down
  q = quit
  h = toggle hidden files
  d = toggle file size
  prefix ■ means folder
  
press any button to continue'''

def main():
    pass

if __name__ == "__main__":
    print('Press enter')

# RETURN FILE SIZE AS A STRING
def file_size(path):
    size = os.stat(path).st_size
    i = 0
    while size > 999:
        size = size / 1000
        i = i+1
    metric = ['b','kb','mb','gb']
    return str(round(size,2)) + ' ' + metric[i]

# LIST OF FOLDERS AND FILES
def directory():
    global hidden
    dirs = sorted([x for x in os.listdir() if os.path.isdir(os.path.abspath(os.getcwd()) + '/' + x) and (hidden or not x.startswith('.') )], key=lambda s: s.lower())
    files = sorted([x for x in os.listdir() if x not in dirs and (hidden or not x.startswith('.') )], key=lambda s: s.lower())
    return dirs + files

# CLEAN TERMINAL
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# INDEX UPDATER
def index_dir():
    global index
    if len(directory()) > 0:
        index = index % len(directory())
    else:
        index = 0

# PRINTING FUNCTION
def dir_printer():
    global index
    clear()
    # path directory
    print('press i for instructions\n\n' + os.path.abspath(os.getcwd()) + '/\n')
    # folders and pointer
    if len(directory()) == 0:
        print('**EMPTY FOLDER**')
    else:
        index_dir()
        temp_sel = directory()[index]
        l = max([len(x) for x in directory()]) + 4 # max length file
        for x in directory():
            if x == temp_sel:
                print('->', end='')
            else:
                print('  ', end='')
            if os.path.isdir(os.path.abspath(os.getcwd()) + '/' + x):
                print('■', end='')
            else:
                print(' ', end='')
            print(x, end=' ')
            if dimension and os.path.isfile(os.path.abspath(os.getcwd()) + '/' + x):
                print(' '*(l-len(x)) + file_size(os.path.abspath(os.getcwd()) + '/' + x))
            else:
                print()

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

dir_printer()

# MAIN ROUTINE
while True:
    index_dir() # update index
    match getch():
        # quit
        case 'q':
            break
        # toggle hidden
        case 'h':
            temp_name = directory()[index]
            hidden = not hidden
            if temp_name in directory(): # update index
                index = directory().index(temp_name)
            else:
                index = 0
        # instructions
        case 'i':
            clear()
            print(instructions)
            getch()
        case 'd':
            dimension = not dimension
        case '\x1b':
            if getch() == '[':
                match getch():
                    # left
                    case 'D':
                        os.chdir('..')
                    # up
                    case 'A' if len(directory()) > 0:
                        index = index - 1
                    # down
                    case 'B' if len(directory()) > 0:
                        index = index + 1
                    # right
                    case 'C' if len(directory()) > 0:
                        selection = os.path.abspath(os.getcwd()) + '/' + directory()[index]
                        if os.path.isdir(selection):
                            os.chdir(selection)
                        elif os.path.isfile(selection):
                            clear()
                            print(selection)
                            break
                    case _:
                        pass
        case _:
            pass
    dir_printer()

os.chdir(local_folder)
