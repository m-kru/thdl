import re
from . import checker


class ClockChecker(checker.Checker):

    CLOCK_PORT_MAP_WITH_FREQUENCIES = re.compile(
        r"cl(oc)?k_?(\d+).*=>.*cl(oc)?k_?(\d+)"
    )

    def __init__(self):
        super(ClockChecker, self).__init__()

    def check(self, line):
        """Check line for stupid clock mistakes.

        Parameters:
        -----------
        line :
            Line read from file.

        Returns
        -------
            Reference to string if violation is found. Otherwise None.
        """
        match = self.CLOCK_PORT_MAP_WITH_FREQUENCIES.search(line)
        if match:
            if match[2] != match[4]:
                return self.message("Clock frequency mismatch!")
