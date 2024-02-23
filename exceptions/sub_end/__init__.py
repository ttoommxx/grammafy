"""end routines module intitialiser"""
from typing import NoReturn, TypeVar

EnvVar = TypeVar("EnvVar")

# ----------------------------------------
# BULTI-IN FUNCTIONS
# ----------------------------------------


def _proof(ENV: EnvVar) -> NoReturn:
    """add proof to CLEAN"""
    ENV.clean.add("■\n")


# ----------------------------------------
# VARIABLES
# ----------------------------------------

from exceptions.sub_end.end_custom import void_c

# every end command is automatically void, void_c can be use to invalidate bulti-in end commands

from exceptions.sub_end.end_custom import dic_commands_c

dic_commands = {"proof": _proof}

# ----------------------------------------
# INTERPRETER
# ----------------------------------------


def interpret(ENV: EnvVar) -> NoReturn:
    """custom interpreter for the end routine"""
    if ENV.command in void_c:
        pass
    elif ENV.command in dic_commands_c:
        dic_commands_c[ENV.command](ENV)
    elif ENV.command in dic_commands:
        dic_commands[ENV.command](ENV)
