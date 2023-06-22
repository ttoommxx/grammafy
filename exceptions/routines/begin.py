import os

# behave similarly to the main, just create a list of what could be
exceptions = (e[:-3] for e in os.listdir("./exceptions/subroutines/begin/"))

with open("./exceptions/subroutines/void_begin.txt") as void_begin_file, open("./exceptions/subroutines/void_begin_custom.txt") as void_begin_custom_file:
    void_begin = [line.strip() for line in void_begin_file.readlines()] + [line.strip() for line in void_begin_custom_file.readlines()]

i = SOURCE[-2].find("}", SOURCE[-1]) # right next after the brackets
asterisk =  SOURCE[-2][i-1] == "*"
command_name = SOURCE[-2][ SOURCE[-1]+1:i-asterisk ] # remove asterisk if any
SOURCE[-1] = i+1

if os.path.exists(f"./exceptions/subroutines/begin_custom/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/begin_custom/{command_name}.py").read())
elif os.path.exists(f"./exceptions/subroutines/begin/{command_name}.py"):
    exec(open(f"./exceptions/subroutines/begin/{command_name}.py").read())
elif command_name not in void_begin:
    # do someething here like skip the command entirely by looking at where \end{command_name + asterisk if any} is. proble is incapsulated commands, so maybe best strategy is do nothing
    list_log_command.add(command_name)
    if asterisk:
        command_name = command_name + "*"
    i = SOURCE[-1]
    j = i
    j_alert = i
    while i >= j and j_alert>-1:
        i = SOURCE[-2].find("\\end{" + command_name + "}",i) + 6 + len(command_name)
        j_alert = SOURCE[-2].find("\\begin{" + command_name + "}",j)
        j = j_alert + 8 + len(command_name)
        
    SOURCE[-1] = i
    