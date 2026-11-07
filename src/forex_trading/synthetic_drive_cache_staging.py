"""M2/P0.8: Google Drive-oriented synthetic cache staging and mixed-scope replay.

All "Drive" objects are an IN-MEMORY simulator of immutable chunk names,
checksums, manifest generations and a publish pointer. NO Google API, disk,
network, authentication, real price feed, persistence, encryption or cross-
process atomicity is provided. Google Drive is an APPROVED DESIGN DESTINATION,
not an approved real-data writer without independently verified vendor rights.

The test oracle supplies complete synthetic histories. Real adapters must
fetch only bounded selected partitions and cannot know unqueried corrections.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
from re import fullmatch
from typing import Mapping

from .cache_core import (
    CandleSnapshot, IncrementalPolicy, RefreshMode,
    plan_incremental_refresh, reconcile_closed_delta,
)
from .cache_storage_review import (
    SyntheticGenerationManifest, make_synthetic_generation,
    validate_synthetic_generation_chain,
)
from .market_data import BarSide, Timeframe
from .quotes import ensure_utc
from .scan_selection import ScanMode, ScanSelection, plan_scan_selection


class SyntheticCacheAction(str, Enum):
    BOOTSTRAP = "BOOTSTRAP"
    DELTA_COMMITTED = "DELTA_COMMITTED"
    REUSE_UNCHANGED = "REUSE_UNCHANGED"


@dataclass(frozen=True, slots=True)
class SyntheticChunk:
    """Chunk and snapshot content exist ONLY inside this in-memory test process."""
    name: str
    snapshot: CandleSnapshot
    partition_fingerprint: str
    snapshot_fingerprint: str


@dataclass(frozen=True, slots=True)
class MixedScanResult:
    selection: ScanSelection
    bootstrapped_streams: int
    delta_plans: int
    source_rows_selected_from_oracle: int
    appended: int
    revised: int
    unchanged_streams: int
    simulated_new_chunk_writes: int
    unchanged_existing_streams: int
    # Explicitly zero: fixture row counts are NOT upstream HTTP metrics.
    actual_drive_api_calls: int = 0
    actual_vendor_api_calls: int = 0
    may_store_real_market_data: bool = False
    may_trade: bool = False


class SyntheticDriveCacheStaging:
    """Deterministic metadata+in-memory chunks, *not* Google Drive IO.

    The root folder ID is a configuration pointer only. Each partition has an
    independent active generation and append-only history; publishing a new
    generation never overwrites another pair. No metadata-only pointer can
    establish a trusted anti-rollback witness or a distributed lock.
    """

    def __init__(self, root_folder_id: str):
        if not isinstance(root_folder_id, str) or not fullmatch(
            r"[A-Za-z0-9_-]{10,128}", root_folder_id
        ):
            raise ValueError("INVALID_DRIVE_FOLDER_REFERENCE")
        self.root_folder_id = root_folder_id
        self._chunks: dict[str, SyntheticChunk] = {}
        self._histories: dict[str, list[SyntheticGenerationManifest]] = {}
        self._active_names: dict[str, str] = {}
        self._active_digests: dict[str, str] = {}
        self.read_partition_ids: list[str] = []
        self.write_partition_ids: list[str] = []

    @property
    def partition_count(self) -> int:
        return len(self._active_names)

    @property
    def simulated_chunk_count(self) -> int:
        return len(self._chunks)

    def manifest_history(self, fingerprint: str) -> tuple[SyntheticGenerationManifest, ...]:
        return tuple(self._histories.get(fingerprint, ()))

    def load(self, partition_fingerprint: str) -> CandleSnapshot | None:
        if not isinstance(partition_fingerprint, str) or not fullmatch(
            r"[a-f0-9]{64}", partition_fingerprint
        ):
            raise ValueError("INVALID_PARTITION_FINGERPRINT")
        self.read_partition_ids.append(partition_fingerprint)
        name = self._active_names.get(partition_fingerprint)
        if name is None:
            return None
        history = self._histories.get(partition_fingerprint, ())
        if not history or self._active_digests.get(partition_fingerprint) != history[-1].manifest_sha256:
            raise ValueError("SIMULATED_ACTIVE_POINTER_OR_HISTORY_CORRUPT")
        for i, manifest in enumerate(history):
            validate_synthetic_generation_chain(
                manifest, history[i - 1] if i else None
            )
        chunk = self._chunks.get(name)
        if chunk is None or (
            chunk.partition_fingerprint != partition_fingerprint
            or chunk.snapshot_fingerprint != history[-1].cache_fingerprint
            or chunk.snapshot.fingerprint != chunk.snapshot_fingerprint
            or chunk.name != name
        ):
            raise ValueError("SIMULATED_CHUNK_MISSING_OR_CORRUPT")
        return chunk.snapshot

    def stage_and_commit(
        self, snapshot: CandleSnapshot, now_utc: datetime,
        *, expected_active_sha256: str | None,
        inject_crash_before_publish: bool = False,
    ) -> bool:
        """Simulated append-only chunk + manifest, then pointer publication.

        expected_active_sha256 is an in-memory optimistic-concurrency check,
        NOT a Drive API CAS guarantee. An orphan staged chunk is not active.
        """
        if not isinstance(snapshot, CandleSnapshot):
            raise TypeError("Typed CandleSnapshot required")
        ensure_utc(now_utc, "now_utc")
        if type(inject_crash_before_publish) is not bool:
            raise TypeError("inject_crash_before_publish must be bool")
        part = snapshot.partition.fingerprint
        current = self._active_digests.get(part)
        if current != expected_active_sha256:
            raise ValueError("SIMULATED_STALE_GENERATION_CONFLICT")
        prev = self._histories[part][-1] if current else None
        if prev is not None and prev.cache_fingerprint == snapshot.fingerprint:
            return False  # no new price data; retain validated immutable chunk

        name = "partitions/" + part + "/chunks/" + sha256(
            (part + ":" + snapshot.fingerprint).encode("ascii")
        ).hexdigest() + ".synthetic"
        chunk = SyntheticChunk(name, snapshot, part, snapshot.fingerprint)
        previous_at_name = self._chunks.get(name)
        if previous_at_name is not None and previous_at_name != chunk:
            # Same name+digest must not change content.
            if (previous_at_name.snapshot.fingerprint != snapshot.fingerprint
                or previous_at_name.partition_fingerprint != part):
                raise ValueError("SYNTHETIC_CONTENT_ADDRESS_COLLISION")
        else:
            self._chunks[name] = chunk
        new = make_synthetic_generation(snapshot, now_utc, prev)
        if inject_crash_before_publish:
            # Orphan chunk exists but neither manifest nor pointer changed.
            raise RuntimeError("SIMULATED_CRASH_BEFORE_PUBLISH")
        # Single-process metadata state update; not actual distributed atomicity.
        self._histories.setdefault(part, []).append(new)
        self._active_names[part] = name
        self._active_digests[part] = new.manifest_sha256
        self.write_partition_ids.append(part)
        return True

    def simulate_corrupt_active_chunk_for_test(self, fingerprint: str) -> None:
        """Negative-path fixture only: deliberately delete referenced chunk."""
        name = self._active_names.get(fingerprint)
        if name is None:
            raise ValueError("NO_ACTIVE_CHUNK_TO_CORRUPT")
        self._chunks.pop(name, None)


def run_mixed_scope_synthetic_drive_scan(
    cache: SyntheticDriveCacheStaging,
    oracle_by_pair: Mapping[str, tuple[CandleSnapshot, ...]],
    universe: tuple[str, ...],
    mode: ScanMode,
    policy: IncrementalPolicy,
    decision_utc: datetime,
    *,
    requested_pairs: tuple[str, ...] = (),
    timeframes: tuple[Timeframe, ...] = (
        Timeframe.M5, Timeframe.M15, Timeframe.H1,
        Timeframe.H4, Timeframe.D1,
    ),
) -> MixedScanResult:
    """Read only selected partitions; keep valid previously committed history.

    For first selected appearance, bootstrap from synthetic oracle; subsequent
    scans query the oracle only over bounded overlap+new windows. For safety
    NO self-declared source-head skip: head=None forces recheck of overlap.
    A real source might revise outside this overlap; remain UNVERIFIED.
    """
    if not isinstance(cache, SyntheticDriveCacheStaging):
        raise TypeError("SyntheticDriveCacheStaging required")
    if not isinstance(oracle_by_pair, Mapping):
        raise TypeError("Typed synthetic oracle mapping required")
    if not isinstance(policy, IncrementalPolicy):
        raise TypeError("IncrementalPolicy required")
    ensure_utc(decision_utc, "decision_utc")
    if (not isinstance(timeframes, tuple) or not timeframes
            or any(not isinstance(tf, Timeframe) for tf in timeframes)
            or len(set(timeframes)) != len(timeframes)):
        raise ValueError("INVALID_EXPECTED_TIMEFRAMES")
    selection = plan_scan_selection(universe, mode, requested_pairs)

    # Preflight selected inputs BEFORE committing any partition: absent BID,
    # ASK or TF must fail closed instead of leaving a partial success.
    selected_groups: list[tuple[CandleSnapshot, ...]] = []
    expected = {(tf, side) for tf in timeframes for side in (BarSide.BID, BarSide.ASK)}
    for pair in selection.selected_pairs:
        if pair not in oracle_by_pair:
            raise ValueError("SELECTED_PAIR_NOT_IN_SYNTHETIC_ORACLE")
        snapshots = oracle_by_pair[pair]
        if not isinstance(snapshots, tuple) or any(
            not isinstance(snapshot, CandleSnapshot) for snapshot in snapshots
        ):
            raise TypeError("PAIR_SNAPSHOTS_MUST_BE_TYPED_IMMUTABLE")
        keys = [(s.partition.timeframe, s.partition.side) for s in snapshots]
        if (len(keys) != len(expected) or len(set(keys)) != len(keys)
                or set(keys) != expected
                or any(s.partition.instrument_version != pair for s in snapshots)):
            raise ValueError("SELECTED_PAIR_BID_ASK_TF_INCOMPLETE_OR_DUPLICATE")
        if any(s.checked_at_utc > decision_utc for s in snapshots):
            raise ValueError("FUTURE_SOURCE_ORACLE")
        selected_groups.append(snapshots)

    bootstrap = delta = rows = appended = revised = unchanged = writes = unchanged_old = 0
    for snapshots in selected_groups:
        for oracle in snapshots:
            existing = cache.load(oracle.partition.fingerprint)
            active_history = cache.manifest_history(oracle.partition.fingerprint)
            expected_digest = active_history[-1].manifest_sha256 if active_history else None
            if existing is None:
                if not oracle.closed_bars:
                    raise ValueError("EMPTY_SYNTHETIC_BOOTSTRAP")
                bootstrap += 1
                rows += len(oracle.closed_bars)
                if cache.stage_and_commit(
                    oracle, decision_utc, expected_active_sha256=None
                ):
                    writes += 1
                continue
            plan = plan_incremental_refresh(
                existing, policy, decision_utc,
                supports_bounded_range=True, head=None,
            )
            if plan.mode is not RefreshMode.DELTA_WINDOW:
                raise ValueError("NO_BOUNDED_DELTA_AVAILABLE")
            delta += 1
            bounded_rows = tuple(
                bar for bar in oracle.closed_bars
                if bar.key.bar_start_utc >= plan.from_utc
            )
            rows += len(bounded_rows)
            changed = reconcile_closed_delta(
                existing, bounded_rows, decision_utc,
                new_source_head_claim=oracle.source_head_claim,
            )
            appended += changed.appended
            revised += changed.revised
            if changed.appended or changed.revised:
                if cache.stage_and_commit(
                    changed.snapshot, decision_utc,
                    expected_active_sha256=expected_digest,
                ):
                    writes += 1
            else:
                unchanged += 1
                unchanged_old += 1
    return MixedScanResult(
        selection, bootstrap, delta, rows, appended, revised, unchanged,
        writes, unchanged_old,
    )
