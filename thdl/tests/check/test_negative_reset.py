import unittest
import io

from thdl.check.reset import check

LINES_STUCK_TO_0 = """rst_n => '0',
rst_n=>'0',
rstn => '0'
reset_n_i=>'0',
reset_n => '0',
reset_n_i => '0',
RST_N_I=>'0');
wb_rst_n=> '0',
wb_rst_n_i=> '0',
foo_bar_reset_n => '0',
foo_rstn=>'0',
"""

LINES_MAPPED_TO_POSITIVE = """rst_n => rst,
wb_reset_n => reset,
rstn => resetp,
wb_rst_n => reset);
foo_rst_n_i => rst_i,
"""

LINES_NEGATED_NEGATIVE = """rst_n => not rst_n_i,
resetn => not(rst_n),
rst_i_n => not wb_resetn,
reset_n_i => not rstn);
"""

LINES_VALID ="""rst_n => '1',
rst_n_i => not rst_p_i,
rst_n_i => not(reset_p),
resetn => not wb_rst_i
rst_i_n => not wb_reset,
"""

class TestPositiveReset(unittest.TestCase):
    def test_stuck_to_0(self):
        fh = io.StringIO(LINES_STUCK_TO_0)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Negative reset stuck to '0'!", l)

    def test_mapped_to_positive(self):
        fh = io.StringIO(LINES_MAPPED_TO_POSITIVE)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Negative reset mapped to positive reset!", l)

    def test_negated_negative(self):
        fh = io.StringIO(LINES_NEGATED_NEGATIVE)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Negative reset mapped to negated negative reset!", l)

    def test_valid(self):
        fh = io.StringIO(LINES_VALID)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, None, l)
