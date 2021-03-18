"""
SPDX-License-Identifier: GPL-2.0

Copyright (c) 2021 Michał Kruszewski
"""

import argparse
import generate


def parse_cmd_line_args():
    parser = argparse.ArgumentParser(
        prog="thdl",
        description="thdl is a bunch of tools (hidden under single program) for easing the work with VHDL language."
        "It is (and will always be) based solely on the text processing, no semantic analysis."
        "Such approach draws clear line what might be included and what will never be supported."
        "'t' in 'the thdl' stands for 'text'.",
    )

    subparsers = parser.add_subparsers()

    path_help = "Path to the file or directory."
    "In case of the directory the processing is done for all files and subdirectories in a recursive way."

    check_parser = subparsers.add_parser(
        "check",
        help="Check for extremely dump mistakes such as stucking resets to constant reset value.",
    )
    check_parser.add_argument("path", help=path_help)
#    check_parser.set_defaults(func=check)

    generate_parser = subparsers.add_parser(
        "generate",
        help="Create or update HDL source files based on the directives within existing files.",
    )
    generate_parser.add_argument("path", help=path_help)


def main():
    args = parse_cmd_line_args()
    print("Hello from main!")
    generate.generate()


if __name__ == "__main__":
    main()
