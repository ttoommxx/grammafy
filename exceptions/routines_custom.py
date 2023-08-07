#----------------------------------------
# FUNCTIONS
#----------------------------------------

def print_curly(source, clean, command, folder_path):
    clean.text += "[_]"
    source.move_index("}")

#----------------------------------------
# VARIABLES
#----------------------------------------

dic_commands_c = {
    "citep" : print_curly,
    "eqrefp" : print_curly,
    "refp" : print_curly,
}

void_c = (
    "marker",
    "bookmark",
)


# TEMPLATE
# dic_commands_c = {
#     "{name_command}" : "{name_function}",
# }
