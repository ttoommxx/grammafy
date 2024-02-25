"""custom begin routines"""

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------


def _title(ENV) -> None:
    """add title to CLEAN"""
    ENV.clean.add(ENV.command.title() + ".")


def _thm(ENV) -> None:
    """add theorem to CLEAN"""
    ENV.clean.add("Theorem.")


# ----------------------------------------
# VARIABLES
# ----------------------------------------

dic_commands_c = {
    "assumption": _title,
    "example": _title,
    "exercise": _title,
    "thm": _thm,
}

void_c = ()

# TEMPLATE
# dic_commands_c = {
#     "{name_command}": {name_function},
# }
