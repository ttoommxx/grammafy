#----------------------------------------
# FUNCTIONS
#----------------------------------------

def title(source, clean, command, folder_path):
    clean.add(command.title() + ".")

def thm(source, clean, command, folder_path):
    clean.add("Theorem.")

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
