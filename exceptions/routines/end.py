# fix the issue with the asterisk

import os

exceptions = (e[:-3] for e in os.listdir("./exceptions/subroutines/end/"))

i = source.tex.find("}")

asterisk = source.tex[i-1] == "*"
command_name = source.tex[1:i-asterisk] # remove asterisk if any
# command = "./exceptions/subroutines/end/" + command_name + ".py"

source.move_index("}")

# if os.path.exists(command):
#     exec(open(command,'r').read())


if os.path.exists(f"./exceptions/subroutines/end_custom/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/end_custom/{command_name}.py").read())
elif os.path.exists(f"./exceptions/subroutines/end/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/end/{command_name}.py").read())