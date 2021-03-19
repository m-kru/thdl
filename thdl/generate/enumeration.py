import math
import re


class Enumeration:
    def __init__(self, fh, line):
        line = line.split("--")[0].strip()

        self.identifier = line.split()[1]

        self.values = []
        # Single line declaration
        match = re.match("type\s+\w+\s+is\s*\((.*)\);", line)
        if match:
            self.values = list(map(lambda v: v.strip(), match.group(1).split(",")))
        elif line.endswith("("):
            for line in fh:
                if re.match("^\s*\)\s*;", line):
                    break

                line = line.split("--")[0].strip()

                values = line.split(",")
                for v in values:
                    if v:
                        self.values.append(v.strip())
                if re.match("\)\s*;", line):
                    break
        else:
            raise Exception(f"Unable to parse enumeration declaration: {line}")

        self.length = math.ceil(math.log2(len(self.values)))

    def generate_pkg(self):
        string = (
            "function to_slv (e : " + self.identifier + ") return std_logic_vector;\n\n"
        )

        if self.identifier.startswith("t_") or self.identifier.startswith("T_"):
            tmp = self.identifier[2:]
        else:
            tmp = self.identifier
        name = "to_" + tmp
        string += (
            "function "
            + name
            + " (slv : std_logic_vector("
            + str(self.length - 1)
            + " downto 0)) return "
            + self.identifier
            + ";\n"
        )

        return string

    def generate_pkg_body(self):
        string = (
            "function to_slv (e : " + self.identifier + ") return std_logic_vector is\n"
        )
        string += "begin\n"
        string += "   case e is\n"
        for i, v in enumerate(self.values):
            string += (
                "      when "
                + v
                + ' => return "'
                + bin(i)[2:].zfill(self.length)
                + '";\n'
            )
        string += "   end case;\n"
        string += "end function;\n\n"

        if self.identifier.startswith("t_") or self.identifier.startswith("T_"):
            tmp = self.identifier[2:]
        else:
            tmp = self.identifier
        name = "to_" + tmp
        string += (
            "function "
            + name
            + " (slv : std_logic_vector("
            + str(self.length - 1)
            + " downto 0)) return "
            + self.identifier
            + " is\n"
        )
        string += "begin\n"
        string += "   case slv is\n"
        for i, v in enumerate(self.values):
            string += (
                '      when "'
                + bin(i)[2:].zfill(self.length)
                + '" => return '
                + v
                + ";\n"
            )
        # TODO: Think about more elegant others handling. It should probably assert.
        string += "      when others => return " + self.values[-1] + ";\n"
        string += "   end case;\n"
        string += "end function;\n"

        return string
