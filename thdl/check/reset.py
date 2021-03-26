import re


POSITIVE_RESET_PORT_MAP = re.compile("re?se?t((p?)|((_p)?(_i)?)|(_i_p))?\s*=>")
POSITIVE_RESET = re.compile("re?se?t((p?)|((_p)?(_i)?)|(_i_p))")

NEGATIVE_RESET_PORT_MAP = re.compile("re?se?t((n?)|((_n)?(_i)?)|(_i_n))\s*=>")
NEGATIVE_RESET = re.compile("re?se?t((n?)|((_n)?(_i)?)|(_i_n))")

STARTS_WITH_NOT = re.compile("^not\s*\(?")

ONE = re.compile("'1'")

ZERO = re.compile("'0'")


def check(line):
    """Returns message if violation is found or None."""
    line = line.strip()
    if line.startswith("--"):
        return None

    if POSITIVE_RESET_PORT_MAP.search(line):
        return _positive_reset(line)

    if NEGATIVE_RESET_PORT_MAP.search(line):
        return _negative_reset(line)


def _positive_reset(line):
    assignee = line.split("=>")[1].strip()

    negated = False
    if STARTS_WITH_NOT.search(assignee):
        negated = True

    if ONE.search(assignee) and not negated:
        return "Positive reset stuck to '1'!"

    if NEGATIVE_RESET.search(assignee) and not negated:
        return "Positive reset mapped to negative reset!"


def _negative_reset(line):
    assignee = line.split("=>")[1].strip()

    negated = False
    if STARTS_WITH_NOT.search(assignee):
        negated = True

    if ZERO.search(assignee) and not negated:
        return "Negative reset stuck to '0'!"
