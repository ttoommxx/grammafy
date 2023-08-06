#----------------------------------------
# FUNCTIONS
#----------------------------------------

def title(source, clean, command, folder_path):
    clean.text += command.title() + "."

#----------------------------------------
# VARIABLES
#----------------------------------------

from exceptions.sub_begin import routines_custom

dic_commands_c = {
    "assumption":title,
    "example":title,
    "exercise":title,
    "thm":routines_custom.thm
}

# TEMPLATE
# dic_commands_c = {
#     "{name_command}":"routines_custom.{name_function}",
# }
