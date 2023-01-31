import os, sys, termios, tty

local_folder = os.path.abspath(os.getcwd()) + '/' # save original path
index = 0 # dummy index

def main():
    pass

if __name__ == "__main__":
    print('Press enter')

def directory(): # print folders and files that are not hidden, in cronological order
    dirs = sorted([x for x in os.listdir() if os.path.isdir(os.path.abspath(os.getcwd()) + '/' + x) and not x.startswith('.')], key=lambda s: s.lower())
    files = sorted([x for x in os.listdir() if x not in dirs and not x.startswith('.')], key=lambda s: s.lower())
    return dirs + files

def clear():
    if os.name == 'nt': # clean terminal
        os.system('cls')
    else:
        os.system('clear')

def dir_printer(): # priting function
    global index
    clear()
    # instructions on how to use it
    print('INSTRUCTIONS: (leftArrow = previous folder), (rightArrow = open folder\select file), (upArrow = up), (downArrow = down), (q = quit), (* are folders)\n')
    # path directory
    print(os.path.abspath(os.getcwd()) + '/\n')
    # folders and pointer
    if len(directory()) == 0:
        print('**EMPTY FOLDER**')
    else:
        temp_sel = directory()[index]
        for x in directory():
            if x == temp_sel:
                print('->', end='')
            else:
                print('  ', end='')
            if os.path.isdir(os.path.abspath(os.getcwd()) + '/' + x):
                print('*', end='')
            else:
                print(' ', end='')
            print(x)

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

while True:
    char = getch()
    if len(directory()) != 0:
        if char == '\x1b':
            next_char = getch()
            if next_char == '[':
                next_char = getch()
                if next_char == 'A':
                    # up
                    index = (index - 1) % len(directory())
                elif next_char == 'B':
                    # down
                    index = (index + 1) % len(directory())
                elif next_char == 'C':
                    # right
                    selection = os.path.abspath(os.getcwd()) + '/' + directory()[index]
                    if os.path.isdir(selection):
                        os.chdir(selection)
                    elif os.path.isfile(selection):
                        clear()
                        print(selection)
                        break
                    if len(directory()) > 0:
                        index = index % len(directory())
                    else:
                        index = 0
                elif next_char == 'D':
                    # left
                    os.chdir('..')
                    index = index % len(directory())
        elif char == 'q':
            # q
            break
    else:
        if char == '\x1b':
            next_char = getch()
            if next_char == '[':
                next_char = getch()
                if next_char == 'D':
                    # print("left")
                    os.chdir('..')
                    index = 0
        elif char == 'q':
            # print("q")
            break
    dir_printer()

os.chdir(local_folder)
