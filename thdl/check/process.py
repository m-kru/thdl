import re

from . import file_info

PROCESS_WITH_SENSITIVITY_LIST=re.compile(r"\bprocess\b\s*\(.*\)")
RISING_EDGE=re.compile(r"\brising_edge\b")
FALLING_EDGE=re.compile(r"\bfalling_edge\b")


SILENT = False


inside_synchronous_process = False
clocks_in_sensitivity_list = []
clocks_sensitivity_list_line = None
clocks_sensitivity_list_line_number = None


def check(line, silent=False):
    """Check line for stupid process mistakes.

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
    global inside_synchronous_process
    global clocks_in_sensitivity_list

    SILENT = silent

    if PROCESS_WITH_SENSITIVITY_LIST.search(line):
        inside_synchronous_process = False
        clocks_in_sensitivity_list = []

        if line.startswith("end"):
            return None

        _parse_process_line(line)

    if RISING_EDGE.search(line):
        return _rising_edge(line)

    if FALLING_EDGE.search(line):
        return _falling_edge(line)


def _message(msg):
    if not SILENT:
        print("{}:{}".format(file_info.FILEPATH, file_info.LINE_NUMBER))
        print(file_info.LINE, end='')
        print(msg + "\n")

    return msg


def _parse_process_line(line):
    global inside_synchronous_process
    global clocks_sensitivity_list_line
    global clocks_sensitivity_list_line_number
    global clocks_in_sensitivity_list

    sensitivity_list = line.split(')')[0].split('(')[1].split(',')

    for e in sensitivity_list:
        if 'clk' in e or 'clock' in e:
            inside_synchronous_process = True
            clocks_sensitivity_list_line = file_info.LINE
            clocks_sensitivity_list_line_number = file_info.LINE_NUMBER
            clocks_in_sensitivity_list.append(e.strip())


def _get_clock_from_edge_function(line):
    return line.split('edge')[1].split(')')[0].split('(')[1].strip()


def _rising_edge(line):
    # Ignore typical test bench use cases.
    if line.startswith("wait"):
        return None

    if not inside_synchronous_process:
        print(clocks_in_sensitivity_list)
        return _message("rising_edge function found outside synchronous process")

    clock = _get_clock_from_edge_function(line)
    if clock not in clocks_in_sensitivity_list:
        print(clocks_in_sensitivity_list)
        return _message(
            "'{}' not found in the sensitivity list in line {}:\n{}".format(
                clock, clocks_sensitivity_list_line_number, clocks_sensitivity_list_line)
        )

def _falling_edge(line):
    if not inside_synchronous_process:
        return _message("falling_edge function found outside synchronous process")

    clock = _get_clock_from_edge_function(line)
