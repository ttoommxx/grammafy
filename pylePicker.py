import os, sys, termios, tty, time

local_folder = os.path.abspath(os.getcwd()) + '/' # save original path
index = 0 # dummy index

def main():
    pass

if __name__ == "__main__":
    print('Press enter')

def dir_printer(): # priting function
    global index
    if os.name == 'nt': # clean terminal
        os.system('cls')
    else:
        os.system('clear')
    # instructions on how to use it
    print('INSTRUCTIONS: (leftArrow = previous folder), (rightArrow = open folder\select file), (upArrow = up), (downArrow = down), (q = quit), (* are folders)\n')
    # path directory
    print(os.path.abspath(os.getcwd()) + '/\n')
    # folders and pointer
    if len(os.listdir()) == 0:
        print('**EMPTY FOLDER**')
    for x in os.listdir():
        if os.listdir().index(x) == index:
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
    if len(os.listdir()) != 0:
        if char == '\x1b':
            next_char = getch()
            if next_char == '[':
                next_char = getch()
                if next_char == 'A':
                    # print("up")
                    index = (index - 1) % len(os.listdir())
                elif next_char == 'B':
                    # print("down")
                    index = (index + 1) % len(os.listdir())
                elif next_char == 'C':
                    # print("right")
                    selection = os.path.abspath(os.getcwd()) + '/' + os.listdir()[index]
                    if os.path.isdir(selection):
                        os.chdir(selection)
                    elif os.path.isfile(selection): # MODIFIED HERE
                        if os.listdir()[index][-4:] == '.tex':
                            open(local_folder + 'file_picked','w').write(selection)
                            break
                        else:
                            if os.name == 'nt':
                                os.system('cls')
                            else:
                                os.system('clear')
                            print('Not a .tex file!')
                            time.sleep(1)
                    index = 0
                elif next_char == 'D':
                    # print("left")
                    index = 0
                    os.chdir('..')
        elif char == 'q':
            # print("q")
            break
    else:
        if char == '\x1b':
            next_char = getch()
            if next_char == '[':
                next_char = getch()
                if next_char == 'D':
                    # print("left")
                    index = 0
                    os.chdir('..')
        elif char == 'q':
            # print("q")
            break
    dir_printer()

os.chdir(local_folder)
