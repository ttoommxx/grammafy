"""custom begin routines"""
from typing import NoReturn, TypeVar

EnvVar = TypeVar("EnvVar")

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------


def _title(ENV: EnvVar) -> NoReturn:
    """add title to CLEAN"""
    ENV.clean.add(ENV.command.title() + ".")


def _thm(ENV: EnvVar) -> NoReturn:
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
