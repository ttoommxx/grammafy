import os, sys, termios, tty, time
from platform import system

local_folder = os.path.abspath(os.getcwd()) + '/' # save original path
from settings import *
index = 0 # dummy index
modalities = ['-picker','-manager']

def instructions(mode):
    if mode == '-manager':
        print('''file manager - INSTRUCTIONS:

    leftArrow = previous folder
    rightArrow = open folder
    upArrow = up
    downArrow = down
    q = quit
    h = toggle hidden files
    d = toggle file size
    t = toggle time last modified
    m = change ordering
    e = edit using command-line editor
    enter = open using the default application launcher

    prefix ■ means folder

press any button to continue''')
    elif mode == '-picker':
        print('''file picker - INSTRUCTIONS:

    leftArrow = previous folder
    rightArrow = open folder
    upArrow = up
    downArrow = down
    q = quit
    h = toggle hidden files
    d = toggle file size
    t = toggle time last modified
    m = change ordering
    enter = select file
    
    prefix ■ means folder

press any button to continue''')

# UPDATE INDEX DIRECTORY
def index_dir():
    global index
    if len(directory()) > 0: # first of all update index
        index = index % len(directory())
    else:
        index = 0

# RETURN FILE SIZE AS A STRING
def file_size(path):
    size = os.lstat(path).st_size
    i = 0
    while size > 999:
        size = size / 1000
        i = i+1
    metric = ['b','kb','mb','gb']
    return str(round(size,2)) + ' ' + metric[i]

def order_next():
    global settings
    vec = [1, int(settings['dimension'])*(True in [os.path.isfile(x) for x in directory()]), int(settings['time_modified'])*(True in [os.path.isfile(x) for x in directory()])]
    settings['order'] = vec.index(1,settings['order']+1) if 1 in vec[settings['order']+1:] else 0

# LIST OF FOLDERS AND FILES
def directory():
    dirs = []
    files = []
    # order by
    match settings['order']:
        # size
        case 1:
            dirs = sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isdir(x) and (settings['hidden'] or not x.startswith('.') )}.items(), key=lambda x:x[1])
            files = sorted({x:os.lstat(x).st_size for x in os.listdir() if os.path.isfile(x) and (settings['hidden'] or not x.startswith('.') )}.items(), key=lambda x:x[1])
            dirs = [dirs[x][0] for x in range(len(dirs))]
            files = [files[x][0] for x in range(len(files))]
        # time modified
        case 2:
            dirs = sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isdir(x) and (settings['hidden'] or not x.startswith('.') )}.items(), key=lambda x:x[1])
            files = sorted({x:os.lstat(x).st_mtime for x in os.listdir() if os.path.isfile(x) and (settings['hidden'] or not x.startswith('.') )}.items(), key=lambda x:x[1])
            dirs = [dirs[x][0] for x in range(len(dirs))]
            files = [files[x][0] for x in range(len(files))]
        # name
        case _: # 0 and unrecognised values
            dirs = sorted([x for x in os.listdir() if os.path.isdir(x) and (settings['hidden'] or not x.startswith('.') )], key=lambda s: s.lower())
            files = sorted([x for x in os.listdir() if os.path.isfile(x) and (settings['hidden'] or not x.startswith('.') )], key=lambda s: s.lower())
    return dirs + files

# CLEAN TERMINAL
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# PRINTING FUNCTION
def dir_printer():
    clear()
    # path directory
    print('press i for instructions\n\n' + os.path.abspath(os.getcwd()) + '/\n')
    # folders and pointer
    if len(directory()) == 0:
        print('**EMPTY FOLDER**')
    else:
        index_dir()
        temp = directory()[index]
        l_file = max([len(x) for x in directory()]) # max length file
        l_size = max([len(file_size(x)) for x in directory()])
        l_time = 19
        max_l = os.get_terminal_size().columns # length of terminal
        print(' ' + '↓'*(settings['order'] == 0) + ' '*(settings['order'] != 0) + '*NAME*', end='')   
        if settings['dimension'] and True in [os.path.isfile(x) for x in directory()]:
            print(' '*(max_l - max(l_size,6) - (l_time + 2)*(settings['time_modified'] == True) - 10 + (settings['order'] !=1 )) + '↓'*(settings['order'] == 1) + '*SIZE*', end='')
        if settings['time_modified'] and True in [os.path.isfile(x) for x in directory()]:
            print(' '*(max(l_size - 3,3)*(settings['dimension'] == True) + (max_l - 27)*(settings['dimension'] == False) - 1 - (settings['order'] == 2)) + '↓'*(settings['order'] == 2) + '*TIME_M*', end='')
        print()
        for x in directory():
            if x == temp:
                print('→', end='')
            else:
                print(' ', end='')
            if os.path.isdir(x):
                print('■', end='')
            else:
                print(' ', end='')
            print(x, end=' ')
            if settings['dimension'] and os.path.isfile(x):
                print(' '*(max_l - 4 - len(x) - max(l_size,6) - (l_time+2)*(settings['time_modified'] == True)) + file_size(x), end='')
            if settings['time_modified'] and os.path.isfile(x):
                time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.lstat(x).st_mtime)))
                print(' '*( (max(l_size,6) - len(file_size(x)) + 2 )*(settings['dimension'] == True) + (max_l - 23 - len(x))*(settings['dimension'] == False)) + time_stamp, end='')
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

# file manager
def main(mode = '-manager'):
    global index
    global settings
    if mode not in modalities:
        input('mode not recognized, selecting manager..\npress enter to continue')
        mode = '-manager'
    dir_printer()
    while True:
        if len(directory()) > 0:
            selection = directory()[index] # + file name if any
        match getch():
            # quit
            case 'q':
                open(local_folder + 'settings.py','w').write('settings = ' + str(settings)) # save config
                clear()
                os.chdir(local_folder)
                return
            # toggle hidden
            case 'h':
                temp = directory()[index]
                settings['hidden'] = not settings['hidden']
                if len(directory()) > 0:
                    if temp in directory(): # update index
                        index = directory().index(temp)
                    else:
                        index = 0
            # change order
            case 'm':
                if len(directory()) > 0:
                    temp = directory()[index]
                order_next()
                if len(directory()) > 0:
                    index = directory().index(temp)
            # instructions
            case 'i':
                clear()
                instructions(mode)
                getch()
            case 't':
                settings['time_modified'] = not settings['time_modified']
            # size
            case 'd':
                settings['dimension'] = not settings['dimension']
            # command-line editor
            case 'e' if len(directory()) > 0 and mode == '-manager':
                match system():
                    case 'Linux':
                        os.system('$EDITOR ' + selection)
                    case 'Windows':
                        clear()
                        print('Windows does not have any built-in command line editor, press any button to continue')
                        getch()
                    case 'Darwin':
                        os.system('open -e ' + selection)
                    case _:
                        clear()
                        print('system not recognised, press any button to continue')
                        getch()
            case '\r' if len(directory()) > 0:
                if mode == '-picker' and os.path.isfile(selection):
                    path = os.getcwd() + '/' + selection 
                    os.chdir(local_folder)
                    return path
                elif mode == '-manager':
                    match system():
                        case 'Linux':
                            os.system('xdg-open ' + selection)
                        case 'Windows':
                            os.system(selection)
                        case 'Darwin':
                            os.system('open ' + selection)
                        case _:
                            clear()
                            print('system not recognised, press any button to continue')
                            getch()
            case '\x1b':
                if getch() == '[':
                    match getch():
                        # up
                        case 'A' if len(directory()) > 0:
                            index = index - 1
                        # down
                        case 'B' if len(directory()) > 0:
                            index = index + 1
                        # right
                        case 'C' if len(directory()) > 0:
                            if os.path.isdir(selection):
                                os.chdir(selection)
                        # left
                        case 'D':
                            os.chdir('..')
                        case _:
                            pass
            case _:
                pass
        dir_printer()

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except:
        main()
    
