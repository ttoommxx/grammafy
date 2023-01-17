import os,sys # import time if need to debug, time.sleep(seconds), remove sys once stopped debugging
from tkinter import filedialog # graphical interface for fetching the .tex file

import useful_fun

aggro = input('Run in aggressive mode? Y/N \n').lower()

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
newText = ''

# a dictionary of hereditable parameters when running the routines
dicSub = {'readText':str, 'writeText':str, 'path_main':str}

# read main file latex
text = open(file_path, 'r')
oldText = text.read()
text.close()

# find the beginning of the document
if '\\begin{document}' not in oldText:
    print("\\begin{document} not found")
    i = 0 # we start from the beginning, probably it's an included .tex file
else:
    i = oldText.find('\\begin{document}') + 16 # we start from right after '\\begin{document}'
oldText = oldText[i:]

# the way we run this code is by checking for something we call "interactives" and once we run out of one of them we discard them, so that to save time. However, if we have included some tex files we won't understand whether any of these interacties occur again. So first of all we expand the include

# so far works only when the files to include belong to the same folder
while oldText.find('\include{')>-1:
    i = oldText.find('\include{') # the string will start at position i+9
    j = i+9+oldText[i+9:].find('}')
    include_path = oldText[i+9:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    included_text = open(folder_path + include_path, 'r')
    text = included_text.read()
    included_text.close()
    oldText = oldText[:i] + text + oldText[j+1:]

while oldText.find('\input{')>-1:
    i = oldText.find('\input{') # the string will start at position i+7
    j = i+7+oldText[i+7:].find('}')
    include_path = oldText[i+7:j]
    if include_path[-4:] != '.tex': # if the extension is not present
        include_path = include_path + '.tex'
    included_text = open(folder_path + include_path, 'r')
    text = included_text.read()
    included_text.close()
    oldText = oldText[:i] + text + oldText[j+1:]

# start analysing the text
while any([ oldText.find(x) for x in interactives ]): # if any such element occurs
    while min([ oldText.find(x) for x in interactives ], default = 1) == -1:
        interactives.pop( [ oldText.find(x) for x in interactives ].index(-1) )
    if len(interactives) == 0:
        break
    i = min([ oldText.find(x) for x in interactives ])  # take note of the index of such element 
    
    newText = newText + oldText[:i] # we can immediately add what we skipped before any interactive element
    oldText = oldText[i:] # remove the clean part from oldText
    match oldText[0]:
        case '\\':
            if oldText[1] == '[': # equation
                i = oldText[1:].find('\]') + 2
                newText = newText + '[1]'
                if oldText[:i-2].replace(' ','').replace('\n','')[-1] in [',', ';', '.']: # add punctuation to non-inline equations
                    newText = newText + oldText[:i-2].replace(' ','').replace('\n','')[-1]
                oldText = oldText[i:]
            elif oldText[1] == ' ': # space
                oldText = oldText[1:]
            elif oldText[1] == '\\': # new line
                newText = newText + '\n'
                oldText = oldText[2:]
            elif oldText[1] == '\n': # also new line
                oldText = oldText[1:]
            else:
                i = min( [ oldText.find(x) for x in end_command if oldText.find(x)>-1 ] )  # take note of the index of such element

                command_name = oldText[1:i]
                oldText = oldText[i + (oldText[i]=='*'):]
                if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"): # first I search within custom subroutines
                    dicSub['readText'] = oldText
                    dicSub['writeText'] = newText
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines_custom/" + command_name + ".py").read(),dicSub)
                    oldText = dicSub['readText']
                    newText = dicSub['writeText']
                elif os.path.exists("./exceptions/routines/" + command_name + ".py"): # then I search within built-in subroutines
                    dicSub['readText'] = oldText
                    dicSub['writeText'] = newText
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines/" + command_name + ".py").read(),dicSub)
                    oldText = dicSub['readText']
                    newText = dicSub['writeText']
                elif command_name in void:
                    pass
                elif aggro == 'y': # if in aggressive mode I just remove the command with any adjacent square or curly bracket
                    i = 0
                    while oldText[i] in ['{','[']:
                        i = min([oldText[i:].find(x) for x in ['}',']'] if oldText[i:].find(x) > -1])+1 + i
                    oldText = oldText[i:]
                else:
                    print('"' + command_name + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
                    print(useful_fun.line_printer(oldText,i))
                    break
        case '{':
            oldText = oldText[1:]
        case '}':
            oldText = oldText[1:]
        case '$':
            i = oldText[1:].find('$') + 2 # we are starting from after the first '$'
            newText = newText + '[1]'
            # if oldText[1:i-1].replace(' ','').replace('\n','')[-1] in [',', ';', '.']:
            #     newText = newText + oldText[1:i-1].replace(' ','').replace('\n','')[-1]
            oldText = oldText[i:]
        case '%':
            oldText = oldText[oldText.find('\n') + 1:]
        case _:
            print('Fatal error, unknown interactive')

# clean the file from equations that have bad spacing and newlines
i = 0
while newText[i+3:].find('[1]')>-1:
    i = newText[i+3:].find('[1]') + i+3
    if newText[i-1] == '\n':
        newText = newText[:i-1] + ' ' + newText[i:]
    if newText[i+3] in [',', ';', '.']:
             i=i+1
    if newText[i+3] == '\n':
        newText = newText[:i+3] + ' ' + newText[i+4:]


output_file = open(folder_path + file_name + '_grammafied.txt','w')
output_file.write(newText)
output_file.close()

print('Done :)')
if aggro == 'y':
    print('PS, the program run in aggressive mode and, as such, it could have printed incomplete or incorrect output')