import os
import time
# import time if need to debug, time.sleep(seconds)

# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
# fetch list of commands that should not produce any text output
void_temp = open('./exceptions/void.txt','r')
void = [line[:-1] for line in void_temp.readlines()]
# list of admissible characters for commands
admitted_temp = open('./exceptions/admitted.txt','r')
admitted = [line[:-1] for line in admitted_temp.readlines()]

# this will be the final text
newText = ''

dicSub = {'j':int, 'readText':str, 'writeText':str, 'asterisk':bool}

# read main file latex
text = open('main.tex', 'r')
oldText = text.read()
i=0
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
            else:
                # when find backslash, start reading the command with j
                j=i+1
                # stop when the command has characters that are not admissible for commands
                while oldText[j] in admitted:
                    j=j+1
                # create path
                if oldText[j-1] == '*':
                    command = "./exceptions/routines/" + oldText[i+1:j-1] + ".py"
                else:
                    command = "./exceptions/routines/" + oldText[i+1:j] + ".py"
                if os.path.exists(command):
                    dicSub['j'] = j
                    dicSub['readText'] = oldText[j:]
                    dicSub['writeText'] = newText
                    dicSub['asterisk'] = oldText[j-1] == '*'
                    exec(open(command).read(),dicSub)
                    # after executing the command, update j and newText
                    j = dicSub['j']
                    newText = dicSub['writeText']
                elif oldText[i+1:j] not in void:
                    print('error 404: "' + oldText[i+1:j] + '" not found in ./exceptions/routines/ or ./exceptions/void.txt')
                    break
                i = j
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
        case _:
            newText = newText + oldText[i]
    i=i+1

print(newText)
