#----------------------------------------
# FUNCTIONS
#----------------------------------------

def _title(SOURCE, CLEAN, command, folder_path):
    """ add title to CLEAN """
    CLEAN.add(command.title() + ".")

def _thm(SOURCE, CLEAN, command, folder_path):
    """ add theorem to CLEAN """
    CLEAN.add("Theorem.")

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
