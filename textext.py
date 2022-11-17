import sys, os
# import time if need to debug, time.sleep(seconds)

sys.path.append('./modules')
import easygui

file_path = easygui.fileopenbox()
i=1
while file_path[-i] != '\\':
    i=i+1
folder_path = file_path[:-i+1]


# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
exceptions_custom = [e[:-3] for e in os.listdir('./exceptions/routines_custom/')]

# fetch list of commands that should not produce any text output
void_temp = open('./exceptions/void.txt','r')
void = [line[:-1] for line in void_temp.readlines()]
void_temp.close()

# list of admissible characters for commands
admitted_temp = open('./exceptions/admitted.txt','r')
admitted = [line[:-1] for line in admitted_temp.readlines()]
admitted_temp.close()

# this will be the final text
newText = ''

dicSub = {'j':int, 'readText':str, 'writeText':str, 'asterisk':bool, 'path_main':str}

# read main file latex
text = open(file_path, 'r')
oldText = text.read()
text.close()

i=0
# find the beginning of the document document
while oldText[i:i+16] != '\\begin{document}':
    i=i+1
i=i+16

while i<len(oldText):
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
            elif oldText[i+1] == '\\':
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
                    print('error 404: "' + oldText[i+1:j] + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
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

output_file = open(folder_path + 'main_grammafied.txt','w')
output_file.write(newText)
output_file.close()