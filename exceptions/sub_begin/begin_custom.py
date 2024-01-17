#----------------------------------------
# FUNCTIONS
#----------------------------------------

def _title(source, clean, command, folder_path):
    """ add title to clean """
    clean.add(command.title() + ".")

def _thm(source, clean, command, folder_path):
    """ add theorem to clean """
    clean.add("Theorem.")

#----------------------------------------
# VARIABLES
#----------------------------------------

dic_commands_c = {
    "assumption":_title,
    "example":_title,
    "exercise":_title,
    "thm":_thm
}

void_c = (
    
)

# TEMPLATE
# dic_commands_c = {
#     "{name_command}": {name_function},
# }
