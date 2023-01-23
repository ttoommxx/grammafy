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
interactives = ['\\','{','}','$','%','~']

# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
exceptions_custom = [e[:-3] for e in os.listdir('./exceptions/routines_custom/')]

# fetch list of commands that should not produce any text output
void = [line[:-1] for line in open('./exceptions/void.txt','r').readlines()] + [line[:-1] for line in open('./exceptions/void_custom.txt','r').readlines()] # put them together as it doesn't make a difference, there is no overriding

# list of admissible characters for commands
end_command = [' ','{','}','.',',',':',';','*','[',']','(',')','$','\\','\n']

# initialise the final text
CLEAN = ''

# copy the main .tex file to a string
SOURCE = open(file_path, 'r').read()

# find the beginning of the document
if '\\begin{document}' not in SOURCE:
    print("\\begin{document} missing")
    i = 0 # we start from the beginning, probably it's an included .tex file
else:
    i = SOURCE.find('\\begin{document}') + 16 # we start from right after '\\begin{document}'
SOURCE = SOURCE[i:]

# the way we run this code is by checking for something we call "interactives" and once we run out of one of them we discard them, so that to save time. However, if we have included some tex files we won't understand whether any of these interacties occur again. So first of all we expand the include

# so far works only when the files to include belong to the same folder
while SOURCE.find('\include{')>-1:
    i = SOURCE.find('\include{') # the string will start at position i+9
    j = SOURCE.find('}',i+9)
    include_path = SOURCE[i+9:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    SOURCE = SOURCE[:i] + open(folder_path + include_path, 'r').read() + SOURCE[j+1:]

while SOURCE.find('\input{')>-1:
    i = SOURCE.find('\input{') # the string will start at position i+7
    j = SOURCE.find('}',i+7)
    include_path = SOURCE[i+7:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    SOURCE = SOURCE[:i] + open(folder_path + include_path, 'r').read() + SOURCE[j+1:]

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
                i = SOURCE.find('\]',1) + 3
                CLEAN = CLEAN + '[1]'
                if SOURCE[:i-3].replace(' ','').replace('\n','')[-1] in [',', ';', '.']: # add punctuation to non-inline equations
                    CLEAN = CLEAN + SOURCE[:i-3].replace(' ','').replace('\n','')[-1]
                SOURCE = SOURCE[i:]
            elif SOURCE[1] == '&':
                CLEAN = CLEAN + '&'
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == ' ': # space
                SOURCE = SOURCE[1:]
            elif SOURCE[1] == '"':
                CLEAN = CLEAN + '"'
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == '\\': # new line
                CLEAN = CLEAN + '\n'
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == "'":
                if SOURCE[2] in ['a','e','i','o','u']:
                    CLEAN = CLEAN + SOURCE[2] + u'\u0301' # unicode encoding
                    SOURCE = SOURCE[3:]
                else:
                    CLEAN = CLEAN + "'"
                    SOURCE = SOURCE[2:]
            else:
                i = min( [ SOURCE.find(x,1) for x in end_command if SOURCE.find(x,1)>-1 ] )  # take note of the index of such element
                command_name = SOURCE[1:i]
                SOURCE = SOURCE[i + (SOURCE[i]=='*'):]
                if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"): # first I search within custom subroutines
                    exec(open("./exceptions/routines_custom/" + command_name + ".py",'r').read())
                elif os.path.exists("./exceptions/routines/" + command_name + ".py"): # then I search within built-in subroutines
                    exec(open("./exceptions/routines/" + command_name + ".py",'r').read())
                elif command_name in void:
                    pass
                else:
                    i = 0 # index for closed brackets
                    while SOURCE[i] in ['{','[']:
                        i = i+1
                        j = i # index for open brackets
                        while i >= j:
                            i = min([SOURCE.find(x,i) for x in ['}',']'] if SOURCE.find(x,i) > -1])+1
                            j = min([SOURCE.find(x,j) for x in ['{','['] if SOURCE.find(x,j) > -1] , default=i+1)+1
                    # the explanation of the above is a little complicated: I look for a (the first) closed bracket and a (the first) open bracket. They must match, otherwise it would contradict the fact that they are the first. I keep doing it until I can't find an open one. So min will be set to i and we would break out of the internal while. As for the external, every time I get out I look for the adjacent bracket and there is another one I iterate!
                    SOURCE = SOURCE[i:]
                    list_aggro.add(command_name)
        case '~':
            SOURCE = SOURCE[1:]
        case '{':
            SOURCE = SOURCE[1:]
        case '}':
            SOURCE = SOURCE[1:]
        case '$':
            if SOURCE[1] == '$':
                i = SOURCE.find('$$',2) + 2
            else: # assuming there are no double dollars within one-dollar equations
                i = SOURCE.find('$',1) + 1
            CLEAN = CLEAN + '[1]'
            # TO DO, ADD COMMAS ETC IF THAT'S HOW THE EQUATION ENDS
            SOURCE = SOURCE[i:]
        case '%':
            SOURCE = SOURCE[SOURCE.find('\n') + 1:]
        case _:
            print('Fatal error, unknown interactive')

# CLEANING ROUTINES
# remove unmatched brackets and tabbing with spaces
CLEAN = CLEAN.replace('[]','').replace('()','').replace('\t',' ')
# remove initial spaces and newlines
while CLEAN[0] in ['\n',' ']:
    CLEAN = CLEAN[1:]
# remove newline+space preliminarly to the cleaning
while '\n ' in CLEAN:
    CLEAN = CLEAN.replace('\n ','\n')
# reset indentation for [1]s
while '\n[1]' in CLEAN or '[1]\n' in CLEAN or '[1],\n' in CLEAN or '[1].\n' in CLEAN or '[1];\n' in CLEAN:
    CLEAN = CLEAN.replace('\n[1]',' [1]').replace('[1]\n','[1] ').replace('[1],\n','[1], ').replace('[1].\n','[1]. ').replace('[1];\n','[1]; ')
# add some space before every [1] in case we have them attached to something else
CLEAN = CLEAN.replace('.[1]','. [1]'.replace(',[1]',', [1]')).replace(';[1]','; [1]')
while '\n\n\n' in CLEAN or '  ' in CLEAN: # remove double lines and double spaces
    CLEAN = CLEAN.replace('\n\n\n','\n\n').replace('  ',' ')

open(folder_path + file_name + '_grammafied.txt','w').write(CLEAN)

if os.path.exists(folder_path + file_name + '_list_unknowns.txt'):
  os.remove(folder_path + file_name + '_list_unknowns.txt')
if os.path.exists(folder_path + file_name + '_list_log_command.txt'):
  os.remove(folder_path + file_name + '_list_log_command.txt')

if any(list_aggro):
    print('Unknown commands, please check ' + file_name + '_list_unknowns.txt')
    open(folder_path + file_name + '_list_unknowns.txt','w').write(str(list_aggro))
if any(list_log_command):
    print('Unknown commands within commands, please check ' + file_name + '_list_log_command.txt')
    open(folder_path + file_name + '_list_log_command.txt','w').write(str(list_log_command))

print('Done :)')

# printing some extra output that will help me open the cleaned file immediately
print(folder_path + file_name + '_grammafied.txt')