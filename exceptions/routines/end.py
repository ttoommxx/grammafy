import os

exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/end/")]

dicSub = {'writeEnd':str, 'asterisk':bool}

t = 1
while readText[t] != '}':
    t = t+1
t = t+1 # skip the end of brackets for begin

if readText[t-2] == '*':
    command = "./exceptions/subroutines/end/" + readText[1:t-2] + ".py"
else:
    command = "./exceptions/subroutines/end/" + readText[1:t-1] + ".py"

if os.path.exists(command):
    dicSub['writeEnd'] = writeText
    dicSub['asterisk'] = readText[t-2] == '*'
    exec(open(command).read(),dicSub)
    writeText = dicSub['writeEnd']
j = j + t
