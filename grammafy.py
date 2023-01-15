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
admitted_temp = open('./exceptions/admitted.txt','r')
admitted = [line[:-1] for line in admitted_temp.readlines()]
admitted_temp.close()

# initialise the final text
newText = ''

# a dictionary of hereditable parameters when running the routines
dicSub = {'j':int, 'readText':str, 'writeText':str, 'asterisk':bool, 'path_main':str}

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
    
    # FROM HERE - devi modificare tutto tenendo in considerazione che bisogna tagliare per intero tutti i comandi
    
    match oldText[i]:
        case '\\':
            if oldText[i+1] == '[': # execute this first to check if I am within an equaiton delimited by \[ ... \]
                i=i+2 # skip the square bracket and start checking characters
                while oldText[i:i+2] != '\\]':
                    i=i+1
                newText = newText + '[1]'
                j = i-1
                while oldText[j] in [' ', '\n']:
                    j = j-1
                if oldText[j] in [',', ';', '.']:
                    newText = newText + oldText[j]
                i=i+1
            elif oldText[i+1] == ' ': # a space
                pass
            elif oldText[i+1] == '\\': # a new line
                newText = newText + '\n'
                i = i+1
            else:
                # when find backslash, start reading the command with j
                j=i+1
                # stop when the command has characters that are not admissible for commands
                while oldText[j] in admitted:
                    j=j+1
                # create path
                if oldText[j-1] == '*': # remove asterisk if it exists at the end of the name
                    command_name = oldText[i+1:j-1]
                else:
                    command_name = oldText[i+1:j]
                if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"):
                    dicSub['j'] = j
                    dicSub['readText'] = oldText[j:]
                    dicSub['writeText'] = newText
                    dicSub['asterisk'] = oldText[j-1] == '*'
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines_custom/" + command_name + ".py").read(),dicSub)
                    # after executing the command, update j and newText
                    oldText = oldText[:j] + dicSub['readText']
                    j = dicSub['j']
                    newText = dicSub['writeText']
                elif os.path.exists("./exceptions/routines/" + command_name + ".py"):
                    dicSub['j'] = j
                    dicSub['readText'] = oldText[j:]
                    dicSub['writeText'] = newText
                    dicSub['asterisk'] = oldText[j-1] == '*'
                    dicSub['path_main'] = folder_path
                    exec(open("./exceptions/routines/" + command_name + ".py").read(),dicSub)
                    # after executing the command, update j and newText
                    oldText = oldText[:j] + dicSub['readText']
                    j = dicSub['j']
                    newText = dicSub['writeText']
                elif command_name not in void:
                    print(oldText[i+1:j] + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
                    # print(line_printer(oldText,i))
                    break
                i = j-1
        case '{':
            pass
        case '}':
            pass
        case '$':
            i=i+1
            if oldText[i] == '$':
                i = i+1
            while oldText[i] != '$':
                i = i+1
            newText = newText + '[1]'
            j = i-1
            while oldText[j] in [' ', '\n']:
                j = j-1
            if oldText[j] in [',', ';', '.']:
                newText = newText + oldText[j]
            if oldText[i+1] == '$':
                i = i+1
        case '%':
            i = i+1
            while i < len(oldText) and oldText[i] != '\n': # comments end when I go to the next line, need to check if I am going out of the string as we might finish the documents with a comment
                i=i+1
        case _:
            newText = newText + oldText[i]
    i=i+1
    oldText = oldText[i:]

# while i<len(oldText):
#     match oldText[i]:
#         case '\\':
#             if oldText[i+1] == '[': # execute this first to check if I am within an equaiton delimited by \[ ... \]
#                 i=i+2 # skip the square bracket and start checking characters
#                 while oldText[i:i+2] != '\\]':
#                     i=i+1
#                 newText = newText + '[1]'
#                 j = i-1
#                 while oldText[j] in [' ', '\n']:
#                     j = j-1
#                 if oldText[j] in [',', ';', '.']:
#                     newText = newText + oldText[j]
#                 i=i+1
#             elif oldText[i+1] == ' ':
#                 pass
#             elif oldText[i+1] == '\\':
#                 newText = newText + '\n'
#                 i = i+1
#             else:
#                 # when find backslash, start reading the command with j
#                 j=i+1
#                 # stop when the command has characters that are not admissible for commands
#                 while oldText[j] in admitted:
#                     j=j+1
#                 # create path
#                 if oldText[j-1] == '*': # remove asterisk if it exists at the end of the name
#                     command_name = oldText[i+1:j-1]
#                 else:
#                     command_name = oldText[i+1:j]
#                 if os.path.exists("./exceptions/routines_custom/" + command_name + ".py"):
#                     dicSub['j'] = j
#                     dicSub['readText'] = oldText[j:]
#                     dicSub['writeText'] = newText
#                     dicSub['asterisk'] = oldText[j-1] == '*'
#                     dicSub['path_main'] = folder_path
#                     exec(open("./exceptions/routines_custom/" + command_name + ".py").read(),dicSub)
#                     # after executing the command, update j and newText
#                     oldText = oldText[:j] + dicSub['readText']
#                     j = dicSub['j']
#                     newText = dicSub['writeText']
#                 elif os.path.exists("./exceptions/routines/" + command_name + ".py"):
#                     dicSub['j'] = j
#                     dicSub['readText'] = oldText[j:]
#                     dicSub['writeText'] = newText
#                     dicSub['asterisk'] = oldText[j-1] == '*'
#                     dicSub['path_main'] = folder_path
#                     exec(open("./exceptions/routines/" + command_name + ".py").read(),dicSub)
#                     # after executing the command, update j and newText
#                     oldText = oldText[:j] + dicSub['readText']
#                     j = dicSub['j']
#                     newText = dicSub['writeText']
#                 elif command_name not in void:
#                     print(oldText[i+1:j] + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
#                     print(line_printer(oldText,i))
#                     break
#                 i = j-1
#         case '{':
#             pass
#         case '}':
#             pass
#         case '$':
#             i=i+1
#             if oldText[i] == '$':
#                 i = i+1
#             while oldText[i] != '$':
#                 i = i+1
#             newText = newText + '[1]'
#             j = i-1
#             while oldText[j] in [' ', '\n']:
#                 j = j-1
#             if oldText[j] in [',', ';', '.']:
#                 newText = newText + oldText[j]
#             if oldText[i+1] == '$':
#                 i = i+1
#         case '%':
#             i = i+1
#             while i < len(oldText) and oldText[i] != '\n': # comments end when I go to the next line, need to check if I am going out of the string as we might finish the documents with a comment
#                 i=i+1
#         case _:
#             newText = newText + oldText[i]
#     i=i+1

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