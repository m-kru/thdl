Overview
--------

THDL is a bunch of tools (hidden under single program) for easing the work with VHDL language.
It is (and will always be) based solely on the text processing, no semantic analysis.
Such approach draws clear line what might be included and what will never be supported.
'T' in the 'THDL' stands for 'Text'.
However, do **not** read THDL as "Text Hardware Description Language" and do **not** treat it as such.
Currently following subcommands are available:

- :code:`check` - checks for extremely dump mistakes such as stucking resets to constant reset values.
- :code:`generate` - creates and updates VHDL source files based on the directives within existing files.

License
=======

The project is licensed under the GPL-2.0 License.
