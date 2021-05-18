import unittest
import io

from thdl.check.process import check


INVALID_PROCESS_0="""process (foo_clk) is
begin
    if rising_edge(bar_clk) then
        processing <= '1';
    end;
end process;
"""

VALID_PROCESS_0="""flipflop_proc: process(RX_RESET_I, RX_FRAMECLK_I)
begin
    if RX_RESET_I = '1' then
        clken_s(j) <= '0';
    elsif rising_edge(RX_FRAMECLK_I) then
        clken_s(j) <= clken_s(j-1);
    end if;
end process;
"""

VALID_PROCESS_1="""activerxUsrClk_proc: process(gtwiz_userclk_rx_reset_int(i), rx_wordclk_sig(i))
begin
  if gtwiz_userclk_rx_reset_int(i) = '1' then
      gtwiz_userclk_rx_active_meta1(i) <= '0';
      gtwiz_userclk_rx_active_meta2(i) <= '0';
      gtwiz_userclk_rx_active_meta3(i) <= '0';
      gtwiz_userclk_rx_active_int(i)   <= '0';
  elsif rising_edge(rx_wordclk_sig(i)) then
      gtwiz_userclk_rx_active_meta1(i) <= '1';
      gtwiz_userclk_rx_active_meta2(i) <= gtwiz_userclk_rx_active_meta1(i);
      gtwiz_userclk_rx_active_meta3(i) <= gtwiz_userclk_rx_active_meta2(i);
      gtwiz_userclk_rx_active_int(i)   <= gtwiz_userclk_rx_active_meta3(i);
  end if;

end process;
"""

class TestPositiveReset(unittest.TestCase):
    def test_invalid_process_0(self):
        fh = io.StringIO(INVALID_PROCESS_0)

        for i, l in enumerate(fh):
            msg = check(l.lower(), silent=True)
            if i == 2:
                self.assertEqual(msg, "'bar_clk' not found in the sensitivity list in line None:\nNone", l)

    def test_valid_process_0(self):
        fh = io.StringIO(VALID_PROCESS_0)

        for i, l in enumerate(fh):
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, None, l)

    def test_valid_process_1(self):
        fh = io.StringIO(VALID_PROCESS_1)

        for i, l in enumerate(fh):
            msg = check(l.lower(), silent=True)
            self.assertEqual(msg, None, l)
