import os

# behave similarly to the main, just create a list of what could be
exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/begin/")]

void_temp = open('./exceptions/subroutines/void_begin.txt','r')
void_custom_temp = open('./exceptions/subroutines/void_begin_custom.txt','r')
void_begin = [line[:-1] for line in void_temp.readlines()] + [line[:-1] for line in void_custom_temp.readlines()]
void_temp.close()
void_custom_temp.close()

dicSub = {'readBegin':str, 'writeBegin':str}

i = readText.find('}')+1 # right next after the brackets
asterisk =  readText[i-2]=='*'
command_name = readText[1:i-1-asterisk] # remove asterisk if any
readText = readText[i:]

if os.path.exists("./exceptions/subroutines/begin_custom/" + command_name + ".py"):
    dicSub['readBegin'] = readText
    dicSub['writeBegin'] = writeText
    exec(open("./exceptions/subroutines/begin_custom/" + command_name + ".py").read(),dicSub)
    writeText = dicSub['writeBegin']
    readText = dicSub['readBegin']
elif os.path.exists("./exceptions/subroutines/begin/" + command_name + ".py"):
    dicSub['readBegin'] = readText
    dicSub['writeBegin'] = writeText
    exec(open("./exceptions/subroutines/begin/" + command_name + ".py").read(),dicSub)
    writeText = dicSub['writeBegin']
    readText = dicSub['readBegin']
elif command_name not in void_begin:
    # do someething here like skip the command entirely by looking at where \end{command_name + asterisk if any} is. proble is incapsulated commands, so maybe best strategy is do nothing
    if asterisk:
        command_name = command_name + '*'
    i = 0
    j = i
    j_alert = i
    while i >= j and j_alert>-1:
        i = i + readText[i:].find('\\end{' + command_name + '}') + 6 + len(command_name)
        j_alert = readText[j:].find('\\begin{' + command_name + '}')
        j = j + j_alert + 8 + len(command_name)
        
    readText = readText[i:]
    log_command['begin'] = command_name
    