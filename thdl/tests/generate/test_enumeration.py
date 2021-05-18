import unittest
import io

from thdl.generate.enumeration import Enumeration

SINGLE_LINE = "type t_my_enum is (ONE, TWO, THREE);"

SINGLE_GOLDEN_PKG = """function to_slv (e : t_my_enum) return std_logic_vector;

function to_my_enum (slv : std_logic_vector(1 downto 0)) return t_my_enum;
"""

SINGLE_GOLDEN_PKG_BODY = """function to_slv (e : t_my_enum) return std_logic_vector is
begin
   case e is
      when ONE => return "00";
      when TWO => return "01";
      when THREE => return "10";
   end case;
end function;

function to_my_enum (slv : std_logic_vector(1 downto 0)) return t_my_enum is
begin
   case slv is
      when "00" => return ONE;
      when "01" => return TWO;
      when "10" => return THREE;
      when others => return THREE;
   end case;
end function;
"""


MULTI_LINE = """type my_enum is (
    foo,
    bar,
    zaz
);
"""

MULTI_GOLDEN_PKG = """function to_slv (e : my_enum) return std_logic_vector;

function to_my_enum (slv : std_logic_vector(1 downto 0)) return my_enum;
"""

MULTI_GOLDEN_PKG_BODY = """function to_slv (e : my_enum) return std_logic_vector is
begin
   case e is
      when foo => return "00";
      when bar => return "01";
      when zaz => return "10";
   end case;
end function;

function to_my_enum (slv : std_logic_vector(1 downto 0)) return my_enum is
begin
   case slv is
      when "00" => return foo;
      when "01" => return bar;
      when "10" => return zaz;
      when others => return zaz;
   end case;
end function;
"""


class TestEnumeration(unittest.TestCase):
    def test_single_line(self):
        fh = io.StringIO(SINGLE_LINE)

        for l in fh:
            line = l
            break

        enum = Enumeration(fh, line)

        pkg = enum.generate_pkg()
        self.assertEqual(pkg, SINGLE_GOLDEN_PKG)

        pkg_body = enum.generate_pkg_body()
        self.assertEqual(pkg_body, SINGLE_GOLDEN_PKG_BODY)

    def test_multi_line(self):
        fh = io.StringIO(MULTI_LINE)

        for l in fh:
            line = l
            break

        enum = Enumeration(fh, line)

        pkg = enum.generate_pkg()
        self.assertEqual(pkg, MULTI_GOLDEN_PKG)

        pkg_body = enum.generate_pkg_body()
        self.maxDiff = None
        self.assertEqual(pkg_body, MULTI_GOLDEN_PKG_BODY)
