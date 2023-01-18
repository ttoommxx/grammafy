# fix the issue with the asterisk

import os

exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/end/")]

i = SOURCE.find('}')+1 # right next after the brackets

asterisk = SOURCE[i-2]=='*'
command_name = SOURCE[1:i-1-asterisk] # remove asterisk if any
command = "./exceptions/subroutines/end/" + command_name + ".py"

SOURCE = SOURCE[i:]

if os.path.exists(command):
    exec(open(command).read())