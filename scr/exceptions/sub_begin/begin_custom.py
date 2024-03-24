"""custom begin routines"""

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------


def _title(env) -> None:
    """add title to CLEAN"""
    env.clean.add(env.command.title() + ".")


def _thm(env) -> None:
    """add theorem to CLEAN"""
    env.clean.add("Theorem.")


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
