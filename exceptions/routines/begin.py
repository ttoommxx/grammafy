import os

# behave similarly to the main, just create a list of what could be
exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/begin/")]

void_begin = [line[:-1] for line in open('./exceptions/subroutines/void_begin.txt','r').readlines()] + [line[:-1] for line in open('./exceptions/subroutines/void_begin_custom.txt','r').readlines()]

i = SOURCE.find('}')+1 # right next after the brackets
asterisk =  SOURCE[i-2]=='*'
command_name = SOURCE[1:i-1-asterisk] # remove asterisk if any
SOURCE = SOURCE[i:]

if os.path.exists("./exceptions/subroutines/begin_custom/" + command_name + ".py"):
    exec(open("./exceptions/subroutines/begin_custom/" + command_name + ".py",'r').read())
elif os.path.exists("./exceptions/subroutines/begin/" + command_name + ".py"):
    exec(open("./exceptions/subroutines/begin/" + command_name + ".py",'r').read())
elif command_name not in void_begin:
    # do someething here like skip the command entirely by looking at where \end{command_name + asterisk if any} is. proble is incapsulated commands, so maybe best strategy is do nothing
    if asterisk:
        command_name = command_name + '*'
    i = 0
    j = i
    j_alert = i
    while i >= j and j_alert>-1:
        i = SOURCE.find('\\end{' + command_name + '}',i) + 6 + len(command_name)
        j_alert = SOURCE.find('\\begin{' + command_name + '}',j)
        j = j_alert + 8 + len(command_name)
        
    SOURCE = SOURCE[i:]
    list_log_command.add(command_name)
    