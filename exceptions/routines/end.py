# fix the issue with the asterisk

import os

exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/end/")]

dicSub = {'writeEnd':str, 'asterisk':bool}

t = readText.find('}')

if readText[t-1] == '*':
    command = "./exceptions/subroutines/end/" + readText[1:t-2] + ".py"
else:
    command = "./exceptions/subroutines/end/" + readText[1:t-1] + ".py"

if os.path.exists(command):
    dicSub['writeEnd'] = writeText
    dicSub['asterisk'] = readText[t-2] == '*'
    exec(open(command).read(),dicSub)
    writeText = dicSub['writeEnd']
j = j + t
