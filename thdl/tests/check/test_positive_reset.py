import unittest
import io

from thdl.check.reset import check

LINES_STUCK_TO_1 = """rst_p => '1',
rst_p=>'1',
reset_p_i=>'1',
rst => '1',
reset => '1',
reset_i => '1',
reset_p_i => '1',
RST_P_I=>'1');
wb_rst_p=> '1',
wb_rst_p_i=> '1',
foo_bar_reset => '1',
"""

LINES_MAPPED_TO_NEGATIVE = """rst_p => rstn,
rstp => rstn,
reset => reset_n_i,
reset_p_i => rst_n);
wb_rst_p=>  rst_n,
wb_rst_p_i=> foo_reset_n,
"""

LINES_NEGATED_POSITIVE ="""rst_p => not rst_p_i,
reset => not(rst_p),
rst_i => not wb_resetp,
"""

LINES_VALID ="""rst_p => '0',
rst_p_i => not rst_n_i,
rst_p_i => not(reset_n),
reset => not wb_rstn_i
rst_i => not wb_resetn,
"""

class TestPositiveReset(unittest.TestCase):
    def test_stuck_to_1(self):
        fh = io.StringIO(LINES_STUCK_TO_1)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Positive reset stuck to '1'!", l)

    def test_mapped_to_negative(self):
        fh = io.StringIO(LINES_MAPPED_TO_NEGATIVE)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Positive reset mapped to negative reset!", l)

    def test_negated_positive(self):
        fh = io.StringIO(LINES_NEGATED_POSITIVE)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, "Positive reset mapped to negated positive reset!", l)

    def test_valid(self):
        fh = io.StringIO(LINES_VALID)

        for l in fh:
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, None, l)
