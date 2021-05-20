import unittest
import io

from thdl.check.process import ProcessChecker


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

VALID_PROCESS_2="""sync_tx : if syc_tx_g generate
    latch_before_gb : process (GBT_TXFRAMECLK_i(i))
    begin
        if (rising_edge(GBT_TXFRAMECLK_i(i))) then
            gbt_txencdata_muxed_r(i) <= gbt_txencdata_muxed(i);
        end if;
    end process latch_before_gb;
end generate sync_tx;
"""

VALID_PROCESS_3="""det_measclk_sp : process (frq_in)
begin
  if (falling_edge(frq_in)) then
    cmeas_alive_resp_r <= cref_alive_check_r;
  end if;
end process det_measclk_sp;
"""


MISSING_SENSITIVITY_LIST="""alarm_handler_trigger : process
begin
  if rising_edge(clk_40_i) then
    alarm_trigger <= '0';
    if alarm_handler_delay_counter_cnt /= x"00000000" then
      if alarm_handler_delay_counter_cnt = x"00000001" then
        alarm_trigger <= '1';
      end if;
      alarm_handler_delay_counter_cnt <= alarm_handler_delay_counter_cnt - 1;
    end if;
    if alarm_handler_ctrl_stb = '1' then
      if alarm_handler_delay_counter = x"00000000" then
        alarm_trigger <= '1';
      else
        alarm_handler_delay_counter_cnt <= alarm_handler_delay_counter;
      end if;
    end if;
    if rst_n_i = '0' then
      alarm_handler_delay_counter_cnt <= x"00000000";
    end if;
  end if;
end process;
"""


process_checker = ProcessChecker()
process_checker.silent = True


class TestProcessEdge(unittest.TestCase):
    def test_invalid_process_0(self):
        fh = io.StringIO(INVALID_PROCESS_0)

        for i, l in enumerate(fh):
            msg = process_checker.check(l.lower())
            if i == 2:
                self.assertEqual(msg, "'bar_clk' not found in the sensitivity list in line None:\nNone", l)
            else:
                self.assertEqual(msg, None, l)

    def test_valid_process_0(self):
        fh = io.StringIO(VALID_PROCESS_0)

        for l in fh:
            msg = process_checker.check(l.lower())
            self.assertEqual(msg, None, l)

    def test_valid_process_1(self):
        fh = io.StringIO(VALID_PROCESS_1)

        for l in fh:
            msg = process_checker.check(l.lower())
            self.assertEqual(msg, None, l)

    def test_valid_process_2(self):
        fh = io.StringIO(VALID_PROCESS_2)

        for l in fh:
            msg = process_checker.check(l.lower())
            self.assertEqual(msg, None, l)

    def test_valid_process_3(self):
        fh = io.StringIO(VALID_PROCESS_3)

        for l in fh:
            msg = process_checker.check(l.lower())
            self.assertEqual(msg, None, l)

    def test_missing_sensitivity_list(self):
        fh = io.StringIO(MISSING_SENSITIVITY_LIST)

        for i, l in enumerate(fh):
            msg = process_checker.check(l.lower())
            if i == 2:
                self.assertEqual(msg, "'clk_40_i' found in the edge function, but the sensitivity list is missing in line None:\nNone", l)
            else:
                self.assertEqual(msg, None, l)
