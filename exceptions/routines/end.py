# fix the issue with the asterisk

import os

exceptions = (e[:-3] for e in os.listdir("./exceptions/subroutines/end/"))

i = SOURCE[-2].find("}", SOURCE[-1])+1 # right next after the brackets

asterisk = SOURCE[-2][i-2] == "*"
command_name = SOURCE[-2][SOURCE[-1]+1:i-1-asterisk] # remove asterisk if any
# command = "./exceptions/subroutines/end/" + command_name + ".py"

SOURCE[-1] = i

# if os.path.exists(command):
#     exec(open(command,'r').read())


if os.path.exists(f"./exceptions/subroutines/end_custom/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/end_custom/{command_name}.py").read())
elif os.path.exists(f"./exceptions/subroutines/end/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/end/{command_name}.py").read())