import os
#import time if need to debug, time.sleep(seconds)

#create a list of existing exceptions
exceptions = [e[:-3] for e in os.listdir("./Exceptions/subroutines/")]

#this will be the final text
newText = ''

dicSub = {'j':int, 'readText':str, 'writeText':str}
#list of admissible characters for commands
admissibleList = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','*']

#read main file latex
text = open('main.tex', 'r')
oldText = text.read()
i=0
while i<len(oldText):
    if oldText[i] == '\\':
        #when find backslash, start reading the command with j
        j=i+1
        #stop when the command has characters that are not admissible for commands
        while oldText[j] in admissibleList:
            j=j+1
        #create path
        command = "./Exceptions/subroutines/" + oldText[i+1:j] + ".py"
        if os.path.exists(command):
            dicSub['j'] = j
            dicSub['readText'] = oldText[j:]
            dicSub['writeText'] = newText
            exec(open(command).read(),dicSub)
            #after executing the command, update j and newText
            j = dicSub['j']
            newText = dicSub['writeText']
        else:
            print('error 404: "' + oldText[i+1:j] + '" not found in ./Exceptions/subroutines/')
            break
        i = j
    else:
        newText = newText + oldText[i]
    i=i+1

print(newText)
