"""
SPDX-License-Identifier: GPL-3.0-or-later

Copyright (c) 2021 Michał Kruszewski
"""

import argparse
import pathlib
import os
import sys

from .check import check
from .generate import generate


VERSION = "0.0.6"


def parse_cmd_line_args():
    parser = argparse.ArgumentParser(
        prog="thdl",
        description="thdl is a bunch of tools (hidden under single program) for easing the work with VHDL language."
        " It is (and will always be) based solely on the text processing, no semantic analysis."
        " Such approach draws clear line what might be included and what will never be supported."
        " 't' in the 'thdl' stands for 'text'.",
    )

    parser.add_argument(
        "-v", "--version", help="Display thdl version.", action="version", version=VERSION
    )

    subparsers = parser.add_subparsers()

    path_help = "Path to the file or directory."
    "In case of the directory the processing is done for all files and subdirectories in a recursive way."

    check_parser = subparsers.add_parser(
        "check",
        help="Check for extremely dump mistakes such as stucking resets to constant reset value.",
    )
    check_parser.add_argument("path", help=path_help)
    check_parser.set_defaults(func=check.check)

    generate_parser = subparsers.add_parser(
        "generate",
        help="Create or update VHDL source files based on the directives within existing files.",
    )
    generate_parser.add_argument("path", help=path_help)

    return parser.parse_args()


def get_files_to_work_on(path):
    if not path.startswith("/"):
        path = os.getcwd() + "/" + path

    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for f in pathlib.Path(path).glob("**/*.vhd"):
            files.append(f)
    else:
        raise Exception(f"{args.path} is not a path to file or directory")

    return files


def main():
    args = parse_cmd_line_args()

    files = get_files_to_work_on(args.path)

    sys.exit(args.func(files))


if __name__ == "__main__":
    main()
