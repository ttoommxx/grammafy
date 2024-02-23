"""custom routines"""
from typing import NoReturn, TypeVar

EnvVar = TypeVar("EnvVar")

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------


def _print_curly(ENV: EnvVar) -> NoReturn:
    """add [_] to CLEAN when meeting curly brackets and move to the end of curly brackets"""
    ENV.clean.add("[_]")
    ENV.source.move_index("}")


# ----------------------------------------
# VARIABLES
# ----------------------------------------

dic_commands_c = {
    "citep": _print_curly,
    "eqrefp": _print_curly,
    "refp": _print_curly,
}

void_c = (
    "marker",
    "bookmark",
)


# TEMPLATE
# dic_commands_c = {
#     "{name_command}" : "_{name_function}",
# }
