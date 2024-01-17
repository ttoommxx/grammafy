#----------------------------------------
# FUNCTIONS
#----------------------------------------

def _print_curly(SOURCE, CLEAN, command, folder_path):
    """ add [_] to CLEAN when meeting curly brackets and move to the end of curly brackets """
    CLEAN.add("[_]")
    SOURCE.move_index("}")

#----------------------------------------
# VARIABLES
#----------------------------------------

dic_commands_c = {
    "citep" : _print_curly,
    "eqrefp" : _print_curly,
    "refp" : _print_curly,
}

void_c = (
    "marker",
    "bookmark",
)


# TEMPLATE
# dic_commands_c = {
#     "{name_command}" : "_{name_function}",
# }
