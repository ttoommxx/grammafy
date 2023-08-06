#----------------------------------------
# BULTI-IN FUNCTIONS
#----------------------------------------

def proof(source, clean, command, folder_path):
    clean.text += "■\n"

#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.sub_end.void_custom import void_c

# every end command is automatically void, void_c can be use to invalidate bulti-in end commands

from exceptions.sub_end.dictionary_commands_custom import dic_commands_c

dic_commands = {
    "proof":proof
}

#----------------------------------------
# INTERPRETER
#----------------------------------------

def interpret(source, clean, command, folder_path):
    if command in void_c:
        pass
    elif command in dic_commands_c:
        dic_commands_c[command](source, clean, command, folder_path)
    elif command in dic_commands:
        dic_commands[command](source, clean, command, folder_path)