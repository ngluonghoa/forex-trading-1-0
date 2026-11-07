"""M2/P0.13 — synthetic-only FX BID/ASK and fee/SL/TP execution references.

NOT a broker simulator, trade order, strategy Backtest, vendor data feed,
historically validated fill or permission to store licensed FX data.
Only independently fabricated fill receipts can produce a math-only net PnL.
No account-currency conversion is inferred from instrument quote currency.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum

from .model import ActionIntent, Direction
from .quotes import PriceSide, Quote, QuoteQuality, indicative_price


def _price(x: Decimal) -> Decimal:
    if not isinstance(x,Decimal) or not x.is_finite() or x<=0:
        raise ValueError("Positive finite Decimal price required")
    return x


def _cost(x: Decimal) -> Decimal:
    if not isinstance(x,Decimal) or not x.is_finite() or x<0:
        raise ValueError("Nonnegative explicit synthetic cost required")
    return x


def _utc(x: datetime) -> None:
    if not isinstance(x,datetime) or x.tzinfo is None or x.utcoffset()!=timedelta(0):
        raise ValueError("UTC aware timestamp required")


class FXBarOutcome(str,Enum):
    NO_LEVEL_TOUCH="NO_LEVEL_TOUCH"
    STOP_ONLY="STOP_ONLY"
    TARGET_ONLY="TARGET_ONLY"
    AMBIGUOUS_BOTH="AMBIGUOUS_BOTH"


@dataclass(frozen=True)
class FXSyntheticFill:
    pair: str
    quote_currency: str
    action: ActionIntent
    quote_side: PriceSide
    units: Decimal
    price: Decimal
    event_utc: datetime
    first_known_utc: datetime
    synthetic_only: bool=True

    def __post_init__(self):
        if (not isinstance(self.pair,str) or not self.pair.strip()
                or not isinstance(self.quote_currency,str) or not self.quote_currency.strip()):
            raise ValueError("Explicit synthetic pair and quote currency required")
        if not isinstance(self.action,ActionIntent) or not isinstance(self.quote_side,PriceSide):
            raise TypeError("Explicit FX action and BID/ASK required")
        _price(self.units)
        _price(self.price)
        _utc(self.event_utc)
        _utc(self.first_known_utc)
        if self.first_known_utc<self.event_utc:
            raise ValueError("FX event cannot be known before it occurs")
        required={
            ActionIntent.ENTRY_LONG:PriceSide.ASK,
            ActionIntent.EXIT_LONG:PriceSide.BID,
            ActionIntent.ENTRY_SHORT:PriceSide.BID,
            ActionIntent.EXIT_SHORT:PriceSide.ASK,
        }[self.action]
        if self.quote_side is not required:
            raise ValueError("Wrong price side for FX action intent")
        if self.synthetic_only is not True:
            raise PermissionError("Real broker fill not independently verified")


@dataclass(frozen=True)
class FXSyntheticCosts:
    commission_quote_total: Decimal
    slippage_quote_total: Decimal
    swap_credit_or_debit_quote: Decimal
    synthetic_only: bool=True

    def __post_init__(self):
        _cost(self.commission_quote_total)
        _cost(self.slippage_quote_total)
        if not isinstance(self.swap_credit_or_debit_quote,Decimal) or not self.swap_credit_or_debit_quote.is_finite():
            raise ValueError("Explicit signed swap in quote currency required")
        if self.synthetic_only is not True:
            raise PermissionError("Broker schedule not verified")


@dataclass(frozen=True)
class FXFixtureTradeMetric:
    direction: Direction
    quote_currency: str
    gross_quote_pnl: Decimal
    commission_quote: Decimal
    slippage_quote: Decimal
    swap_quote: Decimal
    net_quote_pnl: Decimal
    fixture_only: bool=True
    executable_fill_verified: bool=False
    validated_backtest: bool=False
    trading_eligible: bool=False


def value_fx_synthetic_trade(entry: FXSyntheticFill, exit: FXSyntheticFill,
                             costs: FXSyntheticCosts, *,
                             as_of_utc: datetime) -> FXFixtureTradeMetric:
    """Math-only quote-currency PnL for independently INJECTED FAKE fills.

    Spread is already embedded in ASK entry/BID exit or BID entry/ASK exit;
    do not subtract it again. Commission, positive slippage and signed swap
    are explicit supplied values; real fills/netting/account conversions OFF.
    """
    _utc(as_of_utc)
    if (not isinstance(entry,FXSyntheticFill) or not isinstance(exit,FXSyntheticFill)
            or not isinstance(costs,FXSyntheticCosts)):
        raise TypeError("Typed fabricated fills and cost policy required")
    if entry.pair!=exit.pair or entry.quote_currency!=exit.quote_currency or entry.units!=exit.units:
        raise ValueError("Same pair/quote units required; partial fills not implemented")
    if entry.event_utc>=exit.event_utc or max(entry.first_known_utc,exit.first_known_utc)>as_of_utc:
        raise ValueError("Reverse chronology or future-known quote")
    if entry.action is ActionIntent.ENTRY_LONG:
        if exit.action is not ActionIntent.EXIT_LONG:
            raise ValueError("Cannot close LONG with SHORT entry")
        direction=Direction.LONG
        gross=(exit.price-entry.price)*entry.units
    elif entry.action is ActionIntent.ENTRY_SHORT:
        if exit.action is not ActionIntent.EXIT_SHORT:
            raise ValueError("Cannot close SHORT with LONG entry")
        direction=Direction.SHORT
        gross=(entry.price-exit.price)*entry.units
    else:
        raise ValueError("Entry must be a real direction, not EXIT")
    net=gross-costs.commission_quote_total-costs.slippage_quote_total+costs.swap_credit_or_debit_quote
    return FXFixtureTradeMetric(direction,entry.quote_currency,gross,
            costs.commission_quote_total,costs.slippage_quote_total,
            costs.swap_credit_or_debit_quote,net)


def inspect_fx_ohlc_exit(*, direction: Direction, entry: Decimal, stop: Decimal,
                         target: Decimal, bid_low: Decimal,bid_high: Decimal,
                         ask_low: Decimal,ask_high: Decimal,
                         bar_close_utc: datetime,bar_known_utc: datetime,
                         as_of_utc: datetime) -> FXBarOutcome:
    """Use the exit-side extremes. No intrabar BID/ASK time path => ambiguous.

    LONG exits on BID; SHORT exits on ASK. MID cannot be executable.
    Full OHLC side/time alignment, spreads, gaps and broker fills not proven.
    """
    if not isinstance(direction,Direction):
        raise TypeError("Direction must be typed LONG/SHORT")
    for x in (entry,stop,target,bid_low,bid_high,ask_low,ask_high):
        _price(x)
    if (bid_low>bid_high or ask_low>ask_high or bid_low>ask_low
            or bid_high>ask_high):
        raise ValueError("Incoherent bid/ask extremes")
    if direction is Direction.LONG and not stop<entry<target:
        raise ValueError("LONG levels require stop<entry<target")
    if direction is Direction.SHORT and not target<entry<stop:
        raise ValueError("SHORT levels require target<entry<stop")
    for x in (bar_close_utc,bar_known_utc,as_of_utc):
        _utc(x)
    if bar_known_utc<bar_close_utc or bar_known_utc>as_of_utc:
        raise ValueError("Future known or unclosed FX bar")
    if direction is Direction.LONG:
        stop_hit=bid_low<=stop
        target_hit=bid_high>=target
    else:
        stop_hit=ask_high>=stop
        target_hit=ask_low<=target
    if stop_hit and target_hit:
        return FXBarOutcome.AMBIGUOUS_BOTH
    if stop_hit:
        return FXBarOutcome.STOP_ONLY
    if target_hit:
        return FXBarOutcome.TARGET_ONLY
    return FXBarOutcome.NO_LEVEL_TOUCH


def require_real_fx_backtest_or_trading(*_args:object,**_kwargs:object)->None:
    raise PermissionError("No licensed historical execution path, brokerage receipt or validated OOS PnL")
