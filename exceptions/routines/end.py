# fix the issue with the asterisk

import os

exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/end/")]

dicSub = {'readEnd':str, 'writeEnd':str}

i = readText.find('}')+1 # right next after the brackets

command_name = readText[1:i-1-(readText[i-2]=='*')] # remove asterisk if any
command = "./exceptions/subroutines/end/" + command_name + ".py"

readText = readText[i:]

if os.path.exists(command):
    dicSub['readEnd'] = readText
    dicSub['writeEnd'] = writeText
    exec(open(command).read(),dicSub)
    writeText = dicSub['writeEnd']
    readText = dicSub['readEnd']
    