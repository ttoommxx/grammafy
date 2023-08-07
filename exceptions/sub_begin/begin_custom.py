#----------------------------------------
# FUNCTIONS
#----------------------------------------

def title(source, clean, command, folder_path):
    clean.text += command.title() + "."

def thm(source, clean, command, folder_path):
    clean.text += "Theorem."

#----------------------------------------
# VARIABLES
#----------------------------------------

dic_commands_c = {
    "assumption":title,
    "example":title,
    "exercise":title,
    "thm":thm
}

void_c = (
    
)

# TEMPLATE
# dic_commands_c = {
#     "{name_command}": {name_function},
# }
