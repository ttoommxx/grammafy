import os

# behave similarly to the main, just create a list of what could be
exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/begin/")]

void_temp = open('./exceptions/subroutines/void_begin.txt','r')
void_begin = [line[:-1] for line in void_temp.readlines()]
void_temp.close()

dicSub = {'t':int, 'readBegin':str, 'writeBegin':str, 'asterisk':bool}

t = 1
while readText[t] != '}':
    t = t+1
t = t+1 # skip the end of brackets for begin

if readText[t-2] == '*':
    command_name = readText[1:t-2]
else:
    command_name = readText[1:t-1]

if os.path.exists("./exceptions/subroutines/begin_custom/" + command_name + ".py"):
    dicSub['t'] = t
    dicSub['readBegin'] = readText[t:]
    dicSub['writeBegin'] = writeText
    dicSub['asterisk'] = readText[t-2] == '*'
    exec(open("./exceptions/subroutines/begin_custom/" + command_name + ".py").read(),dicSub)
    t = dicSub['t']
    writeText = dicSub['writeBegin']
elif os.path.exists("./exceptions/subroutines/begin/" + command_name + ".py"):
    dicSub['t'] = t
    dicSub['readBegin'] = readText[t:]
    dicSub['writeBegin'] = writeText
    dicSub['asterisk'] = readText[t-2] == '*'
    exec(open("./exceptions/subroutines/begin/" + command_name + ".py").read(),dicSub)
    t = dicSub['t']
    writeText = dicSub['writeBegin']
elif command_name not in void_begin:
    print('error 404: "' + readText[1:t-1] + '" not found in ./exceptions/subroutines/begin/ or ./exceptions/subroutines/void_begin.txt')
    # we do a loop to find end of the missing package and skip the section entirely
    k = t
    while readText[k:k+6+len(readText[1:t-1])] != '\\end{'+readText[1:t-1]+'}':
        k = k+1
    t = k+6+len(readText[1:t-1])
j = j + t-1
