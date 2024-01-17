#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def _proof(source, clean, command, folder_path):
    """ add proof to clean """
    clean.add("■\n")

#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.sub_end.end_custom import void_c

# every end command is automatically void, void_c can be use to invalidate bulti-in end commands

from exceptions.sub_end.end_custom import dic_commands_c

dic_commands = {
    "proof":_proof
}

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
    """ custom interpreter for the end routine """
    if command in void_c:
        pass
    elif command in dic_commands_c:
        dic_commands_c[command](source, clean, command, folder_path)
    elif command in dic_commands:
        dic_commands[command](source, clean, command, folder_path)