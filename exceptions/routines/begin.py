import os
import useful_fun

# behave similarly to the main, just create a list of what could be
exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/begin/")]

void_temp = open('./exceptions/subroutines/void_begin.txt','r')
void_custom_temp = open('./exceptions/subroutines/void_begin_custom.txt','r')
void_begin = [line[:-1] for line in void_temp.readlines()] + [line[:-1] for line in void_custom_temp.readlines()]
void_temp.close()
void_custom_temp.close()

dicSub = {'readBegin':str, 'writeBegin':str}

i = readText.find('}')+1 # right next after the brackets
command_name = readText[1:i-1-(readText[i-2]=='*')] # remove asterisk if any

if os.path.exists("./exceptions/subroutines/begin_custom/" + command_name + ".py"):
    dicSub['readBegin'] = readText[i:]
    dicSub['writeBegin'] = writeText
    exec(open("./exceptions/subroutines/begin_custom/" + command_name + ".py").read(),dicSub)
    writeText = dicSub['writeBegin']
    readText = dicSub['readBegin']
elif os.path.exists("./exceptions/subroutines/begin/" + command_name + ".py"):
    dicSub['readBegin'] = readText[i:]
    dicSub['writeBegin'] = writeText
    exec(open("./exceptions/subroutines/begin/" + command_name + ".py").read(),dicSub)
    writeText = dicSub['writeBegin']
    readText = dicSub['readBegin']
elif command_name not in void_begin:
    print(command_name + '" not found in ./exceptions/subroutines/begin/ or ./exceptions/subroutines/void_begin.txt')
    # do someething here like skip the command entirely