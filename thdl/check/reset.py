import re

from . import file_info

POSITIVE_RESET_PORT_MAP = re.compile("re?se?t((p)|(_p)|(_i)|(_p_i)|(_i_p))?\s*=>")
POSITIVE_RESET = re.compile("re?se?t((p)|(_i)|(_p))?")

NEGATIVE_RESET_PORT_MAP = re.compile("re?se?t((n)|(_n)|(_n_i)|(_i_n))\s*=>")
NEGATIVE_RESET = re.compile("re?se?t((n)|(_n)|(_i_n))")

STARTS_WITH_NOT = re.compile("^not\s*\(?")


SILENT = False


def check(line, silent=False):
    """Check line for stupid reset mistakes.

    Parameters:
    -----------
    line :
        Line read from file.
    silent : bool
        Do not print any message, only return it.
        Useful for unit tests.

    Returns
    -------
        Reference to string if violation is found. Otherwise None.
    """
    global SILENT
    SILENT = silent

    line = line.strip()
    if line.startswith("--"):
        return None

    if POSITIVE_RESET_PORT_MAP.search(line):
        return _positive_reset(line)

    if NEGATIVE_RESET_PORT_MAP.search(line):
        return _negative_reset(line)


def _message(msg):
    if not SILENT:
        print("{}:{}".format(file_info.FILEPATH, file_info.LINE_NUMBER))
        print(file_info.LINE, end='')
        print(msg + "\n")

    return msg


def _positive_reset(line):
    assignee = line.split("=>")[1].strip()

    if assignee.startswith("'1'"):
        return _message("Positive reset stuck to '1'!")

    negated = False
    if STARTS_WITH_NOT.search(assignee):
        negated = True

    if NEGATIVE_RESET.search(assignee):
        reset = "negative"
    elif POSITIVE_RESET.search(assignee):
        reset = "positive"
    else:
        return None

    if reset == "negative" and not negated:
        return _message("Positive reset mapped to negative reset!")

    if reset == "positive" and negated:
        return _message("Positive reset mapped to negated positive reset!")


def _negative_reset(line):
    assignee = line.split("=>")[1].strip()

    if assignee.startswith("'0'"):
        return _message("Negative reset stuck to '0'!")

    negated = False
    if STARTS_WITH_NOT.search(assignee):
        negated = True

    if NEGATIVE_RESET.search(assignee):
        reset = "negative"
    elif POSITIVE_RESET.search(assignee):
        reset = "positive"
    else:
        return None

    if reset == "positive" and not negated:
        return _message("Negative reset mapped to positive reset!")

    if reset == "negative" and negated:
        return _message("Negative reset mapped to negated negative reset!")
