import unittest
import io

from check.reset import check

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
wb_rst_p_i=> foo_bar_n,
"""

class TestPositiveReset(unittest.TestCase):
    def test_stuck_to_1(self):
        fh = io.StringIO(LINES_STUCK_TO_1)

        for l in fh:
            msg = check(l.lower())
            self.assertEqual(msg, "Positive reset stuck to '1'!")

    def test_mapped_to_negative(self):
        fh = io.StringIO(LINES_MAPPED_TO_NEGATIVE)

        for l in fh:
            msg = check(l.lower())
            self.assertEqual(msg, "Positive reset mapped to negative reset!")
