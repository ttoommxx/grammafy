"""end routines module intitialiser"""

# ----------------------------------------
# BULTI-IN FUNCTIONS
# ----------------------------------------


def _proof(env) -> None:
    """add proof to CLEAN"""
    env.clean.add("■\n")


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


def interpret(env) -> None:
    """custom interpreter for the end routine"""
    if env.command in void_c:
        pass
    elif env.command in dic_commands_c:
        dic_commands_c[env.command](env)
    elif env.command in dic_commands:
        dic_commands[env.command](env)
