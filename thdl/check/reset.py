import re


POSITIVE_RESET = re.compile("re?se?t((p?)|((_p)?(_i)?)|(_i_p))?\s*=>", re.I)

NEGATIVE_RESET = re.compile("re?se?t(n?)|((_n)?(_i)?)|(_i_n)\s*=>", re.I)


def check(line):
    """Returns message if violation is found or None."""
    line = line.strip()
    if line.startswith("--"):
        return None

    if POSITIVE_RESET.search(line):
        return _positive_reset(line)

    if NEGATIVE_RESET.search(line):
        return _negative_reset(line)


def _positive_reset(line):
    assignee = line.split("=>")[1].strip()
    if assignee.startswith("'1'"):
        return "Positive reset stuck to '1'!"


def _negative_reset(line):
    assignee = line.split("=>")[1].strip()
    if assignee.startswith("'0'"):
        return "Negative reset stuck to '0'!"
