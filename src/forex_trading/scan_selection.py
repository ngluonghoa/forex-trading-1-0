"""M2/P0.7 selectable Forex scan scope; deterministic SYNTHETIC-only routing.

Select instruments BEFORE cache/delta planning. This wrapper does not fetch
quotes, start a scheduler, modify cache, grant data rights, or trade.
A 20-instrument approved catalog must be supplied externally: this module
does NOT pretend the actual trading universe has been source-qualified.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from re import fullmatch

from .cache_core import IncrementalPolicy
from .quotes import ensure_utc
from .synthetic_scan_workload import (
    SyntheticScanFixture, SyntheticSweepReport, run_synthetic_five_minute_sweep,
)


class ScanMode(str, Enum):
    SINGLE = "SINGLE"
    CUSTOM = "CUSTOM"
    ALL = "ALL"


@dataclass(frozen=True, slots=True)
class ScanSelection:
    mode: ScanMode
    universe: tuple[str, ...]
    selected_pairs: tuple[str, ...]
    skipped_pairs: tuple[str, ...]
    # Metadata-only, not a quote-loading plan or permission to use a provider.
    may_fetch_real_data: bool = False
    may_trade: bool = False


@dataclass(frozen=True, slots=True)
class SelectedSyntheticScanReport:
    selection: ScanSelection
    sweep: SyntheticSweepReport
    actual_provider_requests: int = 0
    may_run_real_scan: bool = False


def plan_scan_selection(
    universe: tuple[str, ...],
    mode: ScanMode,
    requested_pairs: tuple[str, ...] = (),
) -> ScanSelection:
    """SINGLE=1; CUSTOM=2..19; ALL=20, with no unselected pairs scanned.

    Validate membership without loading candle histories for all 20 pairs.
    No hardcoded external-source symbol mapping is implied.
    """
    if not isinstance(universe, tuple) or len(universe) != 20:
        raise ValueError("TWENTY_PAIR_CATALOG_REQUIRED")
    if any(
        not isinstance(pair, str)
        or not fullmatch(r"[A-Z][A-Z0-9_]{2,31}", pair)
        for pair in universe
    ):
        raise ValueError("INVALID_CATALOG_INSTRUMENT")
    if len(set(universe)) != 20:
        raise ValueError("DUPLICATE_CATALOG_INSTRUMENT")
    if not isinstance(mode, ScanMode):
        raise TypeError("TYPED_SCAN_MODE_REQUIRED")
    if not isinstance(requested_pairs, tuple):
        raise TypeError("IMMUTABLE_REQUESTED_PAIRS_REQUIRED")
    if any(not isinstance(pair, str) for pair in requested_pairs):
        raise TypeError("INVALID_REQUESTED_PAIR_TYPE")
    if len(set(requested_pairs)) != len(requested_pairs):
        raise ValueError("DUPLICATE_REQUESTED_PAIR")
    if any(pair not in universe for pair in requested_pairs):
        raise ValueError("PAIR_NOT_IN_APPROVED_CATALOG")

    if mode is ScanMode.SINGLE:
        if len(requested_pairs) != 1:
            raise ValueError("SINGLE_REQUIRES_EXACTLY_ONE_PAIR")
        selected = requested_pairs
    elif mode is ScanMode.CUSTOM:
        if not 2 <= len(requested_pairs) <= 19:
            raise ValueError("CUSTOM_REQUIRES_TWO_TO_NINETEEN_PAIRS")
        selected = requested_pairs
    else:
        if requested_pairs:
            raise ValueError("ALL_MODE_TAKES_NO_PAIR_SELECTION")
        selected = universe

    chosen = set(selected)
    return ScanSelection(mode, universe, selected, tuple(
        pair for pair in universe if pair not in chosen
    ))


def run_selected_synthetic_scan(
    fixtures: tuple[SyntheticScanFixture, ...],
    policy: IncrementalPolicy,
    decision_utc: datetime,
    *,
    universe: tuple[str, ...],
    mode: ScanMode,
    requested_pairs: tuple[str, ...] = (),
    supports_bounded_range: bool = True,
) -> SelectedSyntheticScanReport:
    """Dispatch ONLY selected fixtures into the existing L1 delta planner.

    A real adapter must honor the selection *before* issuing source calls.
    Passing a full in-memory oracle here is test scaffolding, not proof that
    an upstream provider/download would avoid reading unrelated instruments.
    Selected pairs require BID and ASK completeness per timeframe as in the
    underlying sweep. Missing selected pairs fail closed, never disappear.
    """
    selection = plan_scan_selection(universe, mode, requested_pairs)
    ensure_utc(decision_utc, "decision_utc")
    if not isinstance(fixtures, tuple):
        raise TypeError("IMMUTABLE_FIXTURES_REQUIRED")
    if not isinstance(policy, IncrementalPolicy):
        raise TypeError("IncrementalPolicy required")
    if type(supports_bounded_range) is not bool:
        raise TypeError("supports_bounded_range must be bool")

    selected_set = set(selection.selected_pairs)
    by_pair: dict[str, list[SyntheticScanFixture]] = {
        pair: [] for pair in selection.selected_pairs
    }
    for fixture in fixtures:
        if not isinstance(fixture, SyntheticScanFixture):
            raise TypeError("Typed SyntheticScanFixture required")
        pair = fixture.cached.partition.instrument_version
        if pair in selected_set:
            by_pair[pair].append(fixture)

    if any(not by_pair[pair] for pair in selection.selected_pairs):
        raise ValueError("SELECTED_PAIR_FIXTURES_MISSING")
    selected_fixtures = tuple(
        fixture for pair in selection.selected_pairs for fixture in by_pair[pair]
    )
    sweep = run_synthetic_five_minute_sweep(
        selected_fixtures, policy, decision_utc,
        supports_bounded_range=supports_bounded_range,
    )
    if sweep.pair_count != len(selection.selected_pairs):
        raise ValueError("SELECTED_PAIR_COUNT_MISMATCH")
    return SelectedSyntheticScanReport(selection, sweep)
