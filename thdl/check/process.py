import re

from . import checker
from . import file_info

class ProcessChecker(checker.Checker):

    PROCESS=re.compile(r"\bprocess\b")
    PROCESS_WITH_SENSITIVITY_LIST=re.compile(r"\bprocess\b\s*\((.*)\)")
    ING_EDGE=re.compile(r"\b(ris|fall)ing_edge\b\s*\((.*)\)")

    def __init__(self):
        super(ProcessChecker, self).__init__()

#        inside_process = False
        sensitivity_list = []
        sensitivity_list_line = None
        sensitivity_list_line_number = None

    def check(self, line):
        """Check line for stupid process mistakes.

        Parameters:
        -----------
        line :
            Line read from file.

        Returns
        -------
            Reference to string if violation is found. Otherwise None.
        """
        match = self.PROCESS_WITH_SENSITIVITY_LIST.search(line)
        if match:
            self.sensitivity_list = []
            self.sensitivity_list_line = file_info.LINE
            self.sensitivity_list_line_number = file_info.LINE_NUMBER

            self._parse_sensitivity_list(match[1])
        elif self.PROCESS.search(line):
            if line.startswith('end'):
                return None

            self.sensitivity_list = []
            self.process_line = file_info.LINE
            self.process_line_number = file_info.LINE_NUMBER

        match = self.ING_EDGE.search(line)
        if match:
            return self._ing_edge(line, match[2])

    def _parse_sensitivity_list(self, list_):
        for e in list_.split(','):
            self.sensitivity_list.append(e.strip())

    def _ing_edge(self, line, signal):
        # Ignore typical test bench use cases.
        if line.startswith("wait"):
            return None

        # Ignore some rare, but synthesizable constructs.
        if "<=" in line and "when" in line:
            return None

#        if not self.inside_process:
#            return self.message("{}_edge function found outside synchronous process".format(edge))

        # Handle some special cases, that are not easily to handle with regex.
        if signal.endswith("))"):
            signal = signal[:-1]
        if signal.endswith(")") and '(' not in signal:
            signal = signal[:-1]

        if not self.sensitivity_list:
            return self.message(
                "'{}' found in the edge function, but the sensitivity list is missing in line {}:\n{}".format(
                    signal, self.process_line_number, self.process_line)
            )

        if signal not in self.sensitivity_list:
            return self.message(
                "'{}' not found in the sensitivity list in line {}:\n{}".format(
                    signal, self.sensitivity_list_line_number, self.sensitivity_list_line)
            )
