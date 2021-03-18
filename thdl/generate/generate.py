import re

from . import record
from . import enumeration

def generate(filepath):
    print("Hello from generate!")
    record.record()

    with open(filepath) as fh:
        _parse_file(fh)


def _parse_file(fh):

    # Indicates whether  "--thdl:generate" tag has been found.
    # It is reset on empty lines and after generations.
    tag_found = False

    for line in fh:
        line = line.strip()

        if line.startswith("--thdl:generate"):
            tag_found = True
            continue
        elif tag_found == False:
            continue

        if not line:
            tag_found = False
            continue

        tag_found = False
        if re.match("type\s+\w+\s+is\s*\(", line, re.I):
            enumeration.Enumeration(fh, line)
#        elif:
        else:
            tag_found = True
