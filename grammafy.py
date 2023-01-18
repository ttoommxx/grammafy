import os,sys # import time if need to debug, time.sleep(seconds), remove sys once stopped debugging
from tkinter import filedialog # graphical interface for fetching the .tex file

# aggessive mode, we are going to store all the skipped command in one .txt file
list_aggro = set()
list_log_command = set()

file_path = filedialog.askopenfilename()
# we now store information on the file path, using tkinter we always have '/', even in Windows
i = file_path.rfind('/') + 1
file_name = file_path[i:-4] # .tex is excluded from file_name
folder_path = file_path[:i]

# types of different "command" headers
interactives = ['\\','{','}','$','%']

# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
exceptions_custom = [e[:-3] for e in os.listdir('./exceptions/routines_custom/')]

# fetch list of commands that should not produce any text output
void_temp = open('./exceptions/void.txt','r')
void_custom_temp = open('./exceptions/void_custom.txt','r')
void = [line[:-1] for line in void_temp.readlines()] + [line[:-1] for line in void_custom_temp.readlines()] # put them together as it doesn't make a difference, there is no overriding
void_temp.close()
void_custom_temp.close()

# list of admissible characters for commands
end_command_temp = open('./exceptions/end_command.txt','r')
end_command = [line[:-1] for line in end_command_temp.readlines()]
end_command.append('\n') # don't know how to add it to the txt file
end_command_temp.close()

# initialise the final text
CLEAN = ''

# read main file latex
text = open(file_path, 'r')
SOURCE = text.read()
text.close()

# find the beginning of the document
if '\\begin{document}' not in SOURCE:
    print("\\begin{document} not found")
    i = 0 # we start from the beginning, probably it's an included .tex file
else:
    i = SOURCE.find('\\begin{document}') + 16 # we start from right after '\\begin{document}'
SOURCE = SOURCE[i:]

# the way we run this code is by checking for something we call "interactives" and once we run out of one of them we discard them, so that to save time. However, if we have included some tex files we won't understand whether any of these interacties occur again. So first of all we expand the include

# so far works only when the files to include belong to the same folder
while SOURCE.find('\include{')>-1:
    i = SOURCE.find('\include{') # the string will start at position i+9
    j = i+9+SOURCE[i+9:].find('}')
    include_path = SOURCE[i+9:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    included_text = open(folder_path + include_path, 'r')
    text = included_text.read()
    included_text.close()
    SOURCE = SOURCE[:i] + text + SOURCE[j+1:]

while SOURCE.find('\input{')>-1:
    i = SOURCE.find('\input{') # the string will start at position i+7
    j = i+7+SOURCE[i+7:].find('}')
    include_path = SOURCE[i+7:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    included_text = open(folder_path + include_path, 'r')
    text = included_text.read()
    included_text.close()
    SOURCE = SOURCE[:i] + text + SOURCE[j+1:]

# start analysing the text
while any([ SOURCE.find(x) for x in interactives ]): # if any such element occurs
    set_interactives = set([ SOURCE.find(x) for x in interactives ])
    set_interactives.discard(-1)
    if len(set_interactives) == 0:
        break
    i = min(set_interactives)
    
    # while min([ SOURCE.find(x) for x in interactives ], default = 1) == -1:
    #     interactives.pop( [ SOURCE.find(x) for x in interactives ].index(-1) )
    # if len(interactives) == 0:
    #     break
    # i = min([ SOURCE.find(x) for x in interactives ])  # take note of the index of such element 
    
    CLEAN = CLEAN + SOURCE[:i] # we can immediately add what we skipped before any interactive element
    SOURCE = SOURCE[i:] # remove the clean part from SOURCE
    match SOURCE[0]:
        case '\\':
            if SOURCE[1] == '[': # equation
                i = SOURCE[1:].find('\]') + 3
                CLEAN = CLEAN + '[1]'
                if SOURCE[:i-3].replace(' ','').replace('\n','')[-1] in [',', ';', '.']: # add punctuation to non-inline equations
                    CLEAN = CLEAN + SOURCE[:i-3].replace(' ','').replace('\n','')[-1]
                SOURCE = SOURCE[i:]
            elif SOURCE[1] == ' ': # space
                SOURCE = SOURCE[1:]
            elif SOURCE[1] == '\\': # new line
                CLEAN = CLEAN + '\n'
                SOURCE = SOURCE[2:]
            else:
                i = min( [ SOURCE.find(x) for x in end_command if SOURCE.find(x)>-1 ] )  # take note of the index of such element
                command_name = SOURCE[1:i]
                SOURCE = SOURCE[i + (SOURCE[i]=='*'):]
                if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"): # first I search within custom subroutines
                    exec(open("./exceptions/routines_custom/" + command_name + ".py").read())
                elif os.path.exists("./exceptions/routines/" + command_name + ".py"): # then I search within built-in subroutines
                    exec(open("./exceptions/routines/" + command_name + ".py").read())
                elif command_name in void:
                    pass
                else:
                    i = 0 # index for closed brackets
                    while SOURCE[i] in ['{','[']:
                        i = i+1
                        j = i # index for open brackets
                        while i >= j:
                            i = min([SOURCE[i:].find(x) for x in ['}',']'] if SOURCE[i:].find(x) > -1])+1 + i
                            j = min([SOURCE[j:].find(x) for x in ['{','['] if SOURCE[j:].find(x) > -1] , default=i)+1 + j
                    # the explanation of the above is a little complicated: I look for a (the first) closed bracket and a (the first) open bracket. They must match, otherwise it would contradict the fact that they are the first. I keep doing it until I can't find an open one. So min will be set to i and we would break out of the internal while. As for the external, every time I get out I look for the adjacent bracket and there is another one I iterate!
                    SOURCE = SOURCE[i:]
                    list_aggro.add(command_name)
        case '{':
            SOURCE = SOURCE[1:]
        case '}':
            SOURCE = SOURCE[1:]
        case '$':
            if SOURCE[1] == '$':
                i = 2 + SOURCE[2:].find('$$') + 2
            else: # assuming there are no double dollars within one-dollar equations
                i = 1 + SOURCE[1:].find('$') + 1
            CLEAN = CLEAN + '[1]'
            # TO DO, ADD COMMAS ETC IF THAT'S HOW THE EQUATION ENDS
            SOURCE = SOURCE[i:]
        case '%':
            SOURCE = SOURCE[SOURCE.find('\n') + 1:]
        case _:
            print('Fatal error, unknown interactive')

# clean the file from equations that have bad spacing and newlines, and empty brackets
i = 0
while CLEAN[i+3:].find('[1]')>-1:
    i = CLEAN[i+3:].find('[1]') + i+3
    if CLEAN[i-1] == '\n':
        CLEAN = CLEAN[:i-1] + ' ' + CLEAN[i:]
    if CLEAN[i+3] in [',', ';', '.']:
             i=i+1
    if CLEAN[i+3] == '\n':
        CLEAN = CLEAN[:i+3] + ' ' + CLEAN[i+4:]

while CLEAN.find('[]')>-1:
    i = CLEAN.find('[]')
    CLEAN = CLEAN[:i] + CLEAN[i+3:]
while CLEAN.find('()')>-1:
    i = CLEAN.find('()')
    CLEAN = CLEAN[:i] + CLEAN[i+3:]



output_file = open(folder_path + file_name + '_grammafied.txt','w')
output_file.write(CLEAN)
output_file.close()

if os.path.exists(folder_path + file_name + '_list_unknowns.txt'):
  os.remove(folder_path + file_name + '_list_unknowns.txt')
if os.path.exists(folder_path + file_name + '_list_log_command.txt'):
  os.remove(folder_path + file_name + '_list_log_command.txt')

if any(list_aggro):
    print('Unknown commands, please check' + file_name + '_list_unknowns.txt')
    output_file = open(folder_path + file_name + '_list_unknowns.txt','w')
    output_file.write(str(list_aggro))
    output_file.close()
if any(list_log_command):
    print('Unknown commands within commands, please check' + file_name + '_list_log_command.txt')
    output_file = open(folder_path + file_name + '_list_log_command.txt','w')
    output_file.write(str(list_log_command))
    output_file.close()

print('Done :)')