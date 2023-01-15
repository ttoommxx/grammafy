import os,sys # import time if need to debug, time.sleep(seconds), remove sys once stopped debugging
from tkinter import filedialog # graphical interface for fetching the .tex file

file_path = filedialog.askopenfilename()
# we now store information on the file path, using tkinter we always have '/', even in Windows
i = file_path.rfind('/') + 1
file_name = file_path[i:-4] # .tex is excluded from file_name
folder_path = file_path[:i]

# the following function prints the line from str file containing the y-th letter
def line_printer(str,y):
    return(str[str.rfind('\n',0,y)+2 : str.find('\n',y)])

# types of different "command" headers
interactives = ['\\','{','}','$','%']

# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
exceptions_custom = [e[:-3] for e in os.listdir('./exceptions/routines_custom/')]

# fetch list of commands that should not produce any text output
void_temp = open('./exceptions/void.txt','r')
void_custom_temp = open('./exceptions/void_custom.txt','r')
void = [line[:-1] for line in void_temp.readlines()] + [line[:-1] for line in void_custom_temp.readlines()]
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
dicSub = {'j':int, 'readText':str, 'writeText':str, 'path_main':str}

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

# start analysing the text
while any([ oldText.find(x) for x in interactives ]): # if any such element occurs
    while min([ oldText.find(x) for x in interactives ], default = 1) == -1:
        interactives.pop( [ oldText.find(x) for x in interactives ].index(-1) )
    if len(interactives) == 0:
        break
    i = min([ oldText.find(x) for x in interactives ])  # take note of the index of such element
    newText = newText + oldText[:i] # we can immediately add what we skipped before any interactive element
    oldText = oldText[i:] # remove the clean part from oldText

    # WARNING - devi modificare tutto tenendo in considerazione che bisogna tagliare per intero tutti i comandi
    
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
            else:
                i = min( [ oldText.find(x) for x in end_command if oldText.find(x)>-1 ] )  # take note of the index of such element
                command_name = oldText[1:i]
                oldText = oldText[i:]
                print(i, oldText[i], command_name)
                input('stop')
                if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"):
                    dicSub['j'] = i
                    dicSub['readText'] = oldText
                    dicSub['writeText'] = newText
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines_custom/" + command_name + ".py").read(),dicSub)
                    # after executing the command, update j and newText
                    oldText = dicSub['readText']
                    j = dicSub['j']
                    newText = dicSub['writeText']
                elif os.path.exists("./exceptions/routines/" + command_name + ".py"):
                    dicSub['j'] = i
                    dicSub['readText'] = oldText
                    dicSub['writeText'] = newText
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines/" + command_name + ".py").read(),dicSub)
                    # after executing the command, update j and newText
                    oldText = dicSub['readText']
                    j = dicSub['j']
                    newText = dicSub['writeText']
                elif command_name not in void:
                    print('"' + command_name + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
                    print(line_printer(oldText,i))
                    break
                i = j-1
                oldText = oldText[i:]
        case '{':
            oldText = oldText[1:]
        case '}':
            oldText = oldText[1:]
        case '$':
            i = oldText[2:].find('$') + ( oldText[oldText[2:].find('$')+1] == '$' ) + 1 # add 1 to the index if this happens to be an equation with double dollar
            newText = newText + '[1]'
            if oldText[:i-1].replace(' ','').replace('\n','').replace('$','')[-1] in [',', ';', '.']:
                newText = newText + oldText[:i-1].replace(' ','').replace('\n','').replace('$','')[-1]
            oldText = oldText[i:]
        case '%':
            oldText = oldText[oldText.find('\n') + 1:]
        case _:
            print('fatal error, the script match an interactive that does not know how to deal with')
    print(oldText[:10])

# after having run my code, I fix all those equations that are followed by '/n'
i = 0
while i+3 < len(newText):
    if newText[i:i+3] == '[1]':
        if newText[i-1] == '\n':
            newText = newText[:i-1] + ' ' + newText[i:]
        if newText[i+3] in [',', ';', '.']:
            i=i+1
        if i+3 < len(newText):
            if newText[i+3] == '\n':
                newText = newText[:i+3] + ' ' + newText[i+4:]
    i = i+1

output_file = open(folder_path + file_name + '_grammafied.txt','w')
output_file.write(newText)
output_file.close()