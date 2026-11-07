"""M2/P0.13: fabricated quote-side FX execution and OHLC ambiguity."""
import unittest
from dataclasses import replace
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from forex_trading.model import ActionIntent, Direction
from forex_trading.quotes import PriceSide
from forex_trading.fx_execution_scenarios import (
    FXSyntheticFill,FXSyntheticCosts,FXBarOutcome,value_fx_synthetic_trade,
    inspect_fx_ohlc_exit,require_real_fx_backtest_or_trading,
)

T=datetime(2026,11,6,10,tzinfo=timezone.utc)
ENTRY=FXSyntheticFill("EURUSD-TEST","USD",ActionIntent.ENTRY_LONG,
    PriceSide.ASK,D("100000"),D("1.2020"),T,T+timedelta(seconds=1))
EXIT=FXSyntheticFill("EURUSD-TEST","USD",ActionIntent.EXIT_LONG,
    PriceSide.BID,D("100000"),D("1.2040"),T+timedelta(minutes=30),T+timedelta(minutes=30,seconds=1))
COSTS=FXSyntheticCosts(D("5"),D("2"),D("-1"))
ASOF=T+timedelta(minutes=31)

class FXSyntheticExecutionTest(unittest.TestCase):
    def trade(self,entry=ENTRY,exit=EXIT,costs=COSTS,asof=ASOF):
        return value_fx_synthetic_trade(entry,exit,costs,as_of_utc=asof)

    def test_long_net_quote_pnl_and_spread_not_double_charged(self):
        r=self.trade()
        self.assertEqual(r.direction,Direction.LONG)
        self.assertEqual(r.gross_quote_pnl,D("200.0000"))
        self.assertEqual(r.net_quote_pnl,D("192.0000"))
        self.assertEqual(r.quote_currency,"USD")
        self.assertFalse(r.trading_eligible)
        self.assertFalse(r.validated_backtest)
        self.assertFalse(r.executable_fill_verified)

    def test_short_bid_entry_ask_exit_math(self):
        short=replace(ENTRY,action=ActionIntent.ENTRY_SHORT,quote_side=PriceSide.BID,
                      price=D("1.2040"))
        cover=replace(EXIT,action=ActionIntent.EXIT_SHORT,quote_side=PriceSide.ASK,
                      price=D("1.2020"))
        r=self.trade(entry=short,exit=cover)
        self.assertEqual(r.direction,Direction.SHORT)
        self.assertEqual(r.net_quote_pnl,D("192.0000"))

    def test_swap_credit_adds_and_debit_subtracts(self):
        self.assertEqual(self.trade(costs=FXSyntheticCosts(D("5"),D("2"),D("3"))).net_quote_pnl,
                         D("196.0000"))
        self.assertEqual(self.trade(costs=FXSyntheticCosts(D("5"),D("2"),D("-3"))).net_quote_pnl,
                         D("190.0000"))

    def test_zero_cost_yields_gross_pnl(self):
        r=self.trade(costs=FXSyntheticCosts(D("0"),D("0"),D("0")))
        self.assertEqual(r.net_quote_pnl,r.gross_quote_pnl)

    def test_wrong_side_on_entry_denied(self):
        with self.assertRaises(ValueError):
            replace(ENTRY,quote_side=PriceSide.BID)

    def test_wrong_side_on_exit_denied(self):
        with self.assertRaises(ValueError):
            replace(EXIT,quote_side=PriceSide.ASK)

    def test_direction_mismatch_rejected(self):
        wrong=replace(EXIT,action=ActionIntent.EXIT_SHORT,quote_side=PriceSide.ASK)
        with self.assertRaises(ValueError):self.trade(exit=wrong)

    def test_mismatched_pair_rejected(self):
        with self.assertRaises(ValueError):
            self.trade(exit=replace(EXIT,pair="GBPUSD-TEST"))

    def test_mismatched_units_rejected(self):
        with self.assertRaises(ValueError):
            self.trade(exit=replace(EXIT,units=D("200000")))

    def test_mismatched_quote_currency_rejected(self):
        with self.assertRaises(ValueError):
            self.trade(exit=replace(EXIT,quote_currency="JPY"))

    def test_future_known_exit_rejected(self):
        with self.assertRaises(ValueError):
            self.trade(asof=T+timedelta(minutes=20))

    def test_event_first_known_chronology_rejected(self):
        with self.assertRaises(ValueError):
            replace(ENTRY,first_known_utc=T-timedelta(seconds=1))

    def test_exit_before_entry_rejected(self):
        with self.assertRaises(ValueError):
            self.trade(exit=replace(EXIT,event_utc=T-timedelta(minutes=1),
                   first_known_utc=T+timedelta(seconds=1)))

    def test_negative_commission_rejected(self):
        with self.assertRaises(ValueError):
            FXSyntheticCosts(D("-1"),D("0"),D("0"))

    def test_nonfinite_swap_rejected(self):
        with self.assertRaises(ValueError):
            FXSyntheticCosts(D("0"),D("0"),D("NaN"))

    def test_real_fill_claim_forbidden(self):
        with self.assertRaises(PermissionError):
            replace(ENTRY,synthetic_only=False)

    def test_exit_inspector_long_uses_bid_not_ask(self):
        self.assertEqual(self.inspect(Direction.LONG,D("1.200"),D("1.195"),D("1.210"),
                D("1.198"),D("1.209"),D("1.200"),D("1.212")),FXBarOutcome.NO_LEVEL_TOUCH)

    def inspect(self,direction,entry,stop,target,bid_low,bid_high,ask_low,ask_high):
        return inspect_fx_ohlc_exit(direction=direction,entry=entry,stop=stop,target=target,
           bid_low=bid_low,bid_high=bid_high,ask_low=ask_low,ask_high=ask_high,
           bar_close_utc=T,bar_known_utc=T+timedelta(seconds=1),
           as_of_utc=T+timedelta(minutes=2))

    def test_exit_long_stop_only(self):
        self.assertEqual(self.inspect(Direction.LONG,D("1.200"),D("1.195"),D("1.210"),
              D("1.190"),D("1.205"),D("1.192"),D("1.207")),FXBarOutcome.STOP_ONLY)

    def test_exit_long_target_only(self):
        self.assertEqual(self.inspect(Direction.LONG,D("1.200"),D("1.195"),D("1.210"),
              D("1.197"),D("1.215"),D("1.199"),D("1.217")),FXBarOutcome.TARGET_ONLY)

    def test_exit_long_ambiguous(self):
        self.assertEqual(self.inspect(Direction.LONG,D("1.200"),D("1.195"),D("1.210"),
              D("1.190"),D("1.215"),D("1.192"),D("1.217")),FXBarOutcome.AMBIGUOUS_BOTH)

    def test_exit_short_uses_ask_extremes(self):
        self.assertEqual(self.inspect(Direction.SHORT,D("1.200"),D("1.215"),D("1.190"),
              D("1.187"),D("1.214"),D("1.189"),D("1.216")),FXBarOutcome.AMBIGUOUS_BOTH)

    def test_ask_only_short_stop_not_bid_high(self):
        self.assertEqual(self.inspect(Direction.SHORT,D("1.200"),D("1.215"),D("1.190"),
              D("1.195"),D("1.216"),D("1.196"),D("1.218")),FXBarOutcome.STOP_ONLY)

    def test_crossed_bid_ask_extremes_denied(self):
        with self.assertRaises(ValueError):
            self.inspect(Direction.LONG,D("1.20"),D("1.19"),D("1.21"),
                         D("1.20"),D("1.22"),D("1.19"),D("1.23"))

    def test_invalid_stop_orientation_denied(self):
        with self.assertRaises(ValueError):
            self.inspect(Direction.SHORT,D("1.20"),D("1.19"),D("1.21"),
                         D("1.19"),D("1.21"),D("1.20"),D("1.22"))

    def test_future_known_exit_bar_denied(self):
        with self.assertRaises(ValueError):
            inspect_fx_ohlc_exit(direction=Direction.LONG,
              entry=D("1.20"),stop=D("1.19"),target=D("1.21"),
              bid_low=D("1.18"),bid_high=D("1.22"),ask_low=D("1.19"),ask_high=D("1.23"),
              bar_close_utc=T,bar_known_utc=T+timedelta(hours=1),
              as_of_utc=T+timedelta(minutes=2))

    def test_live_authorization_denied(self):
        with self.assertRaises(PermissionError):
            require_real_fx_backtest_or_trading()

if __name__=="__main__":
    unittest.main()
