import os
# import time if need to debug, time.sleep(seconds)

# create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir('./exceptions/routines/')]
# fetch list of commands that should not produce any text output
void_temp = open('./exceptions/void.txt','r')
void = [line[1:-1] for line in void_temp.readlines()]
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
    if oldText[i] == '\\':
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
            print('error 404: "' + oldText[i+1:j] + '" not found in ./Exceptions/routines/')
            break
        i = j
    elif oldText[i] != '{' and oldText[i] != '}':
        newText = newText + oldText[i]
    i=i+1

print(newText)
