import unittest
import io

from check.reset import check

LINES_STUCK_TO_1 = """rst_n => '0',
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


class TestPositiveReset(unittest.TestCase):
    def test_stuck_to_0(self):
        fh = io.StringIO(LINES_STUCK_TO_1)

        for l in fh:
            line = l
            msg = check(l)
            self.assertEqual(msg, "Negative reset stuck to '0'!")
