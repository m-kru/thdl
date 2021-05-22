import unittest
import io

from thdl.check.clock import ClockChecker


INVALID = """clk_10=>clk_20,
clk_40_i => clk_160)
clk70 => clk_80
clk_70 => clk80_i
clk70 => clk120
clk70_i => clk120_i,
"""


VALID = """clk_10=>clk,
clk_160_i => clk_160)
wb_clk_i => wb_clk
clk => clk_80
clk80 => clk_80
wb_clk_80_i => clk
"""

clock_checker = ClockChecker()
clock_checker.silent = True


class TestClockFreq(unittest.TestCase):
    def test_invalid(self):
        fh = io.StringIO(INVALID)

        for l in fh:
            msg = clock_checker.check(l.lower())
            self.assertEqual(msg, "Clock frequency mismatch!", l)

    def test_valid(self):
        fh = io.StringIO(VALID)

        for l in fh:
            msg = clock_checker.check(l.lower())
            self.assertEqual(msg, None, l)
