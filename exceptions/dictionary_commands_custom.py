#----------------------------------------
# FUNCTIONS
#----------------------------------------

def print_curly(source, clean, command, folder_path):
    clean.text += "[_]"
    source.move_index("}")

#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions import routines_custom

dic_commands_c = {
    "citep" : print_curly,
    "eqrefp" : print_curly,
    "refp" : print_curly,
}

# TEMPLATE
# dic_commands_c = {
#     "{name_command}" : "routines_custom.{name_function}",
# }
