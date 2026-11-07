"""M2/P0.14 — sealed weekly FOREX fixtures; no market source or cloud I/O.

Combines per-week immutable synthetic windows with authenticated encryption.
Only caller-supplied TEST-* / *-fake / NO_REAL_LICENSE fixture observations
are accepted. The store, generation pointer and witness are IN MEMORY and
cannot protect against real multi-writer rollback or establish licensing.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from hashlib import sha256
import json
import re

from .cache_core import CachePartition, CandleSnapshot, reconcile_closed_delta
from .market_data import (
    BarCoverage, BarLifecycle, BarSide, MarketBar, MarketBarKey,
    Observation, SourceQuality, Timeframe,
)
from .quotes import ensure_utc
from .synthetic_sealed_cache import (
    MAGIC, SealedSyntheticChunk, seal_synthetic_fixture, unseal_synthetic_fixture,
)

SCHEMA = "FX_SYNTHETIC_WEEK_WIRE_V1"
MAX_WINDOWS = 256


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _monday(row: MarketBar) -> str:
    d = row.key.bar_start_utc.date()
    return (d - timedelta(days=d.weekday())).isoformat()


def _only_fake(partition: CachePartition, rows: tuple[MarketBar, ...]) -> None:
    if (partition.rights_policy_ref != "NO-RIGHTS"
            or not partition.provider_id.startswith("TEST-")
            or not partition.instrument_version.endswith("-fake")
            or not rows):
        raise PermissionError("SYNTHETIC_FIXTURE_IDENTITY_REQUIRED")
    if any(b.observation.endpoint != "ONLY_SYNTHETIC"
           or b.observation.license_scope_claim != "NO_REAL_LICENSE"
           for b in rows):
        raise PermissionError("REAL_MARKET_SOURCE_NOT_ALLOWED")


def _row(b: MarketBar) -> dict:
    o, k = b.observation, b.key
    return {
        "start": k.bar_start_utc.isoformat(), "end": k.bar_end_utc.isoformat(),
        "revision": b.revision_number, "known": b.first_known_utc.isoformat(),
        "open": str(b.open), "high": str(b.high),
        "low": str(b.low), "close": str(b.close),
        "lifecycle": b.lifecycle.value, "coverage": b.coverage.value,
        "quality": b.quality.value,
        "stream": o.stream_id, "endpoint": o.endpoint,
        "revision_id": o.revision_id, "raw_sha256": o.raw_sha256,
        "obs_known": o.first_known_utc.isoformat(),
        "retrieved": o.retrieved_at_utc.isoformat(),
        "license": o.license_scope_claim,
    }


def _pack(partition: CachePartition, monday: str, rows: tuple[MarketBar, ...],
          as_of: datetime) -> bytes:
    _only_fake(partition, rows)
    CandleSnapshot(partition, rows, as_of, "SYNTHETIC_SEALED_WEEK_WRITE")
    if any(_monday(b) != monday for b in rows):
        raise ValueError("WEEK_MISMATCH")
    return MAGIC + _canonical({
        "schema": SCHEMA, "synthetic_only": True,
        "partition": partition.fingerprint, "monday": monday,
        "rows": [_row(b) for b in rows],
    })


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("DUPLICATE_JSON_FIELD")
        out[k] = v
    return out


_ROW_KEYS = {
    "start", "end", "revision", "known", "open", "high", "low", "close",
    "lifecycle", "coverage", "quality", "stream", "endpoint", "revision_id",
    "raw_sha256", "obs_known", "retrieved", "license",
}


def _unpack(partition: CachePartition, monday: str, data: bytes,
            as_of: datetime) -> tuple[MarketBar, ...]:
    if not isinstance(data, bytes) or not data.startswith(MAGIC):
        raise ValueError("INVALID_WEEK_MAGIC")
    try:
        obj = json.loads(data[len(MAGIC):].decode("ascii"),
                         object_pairs_hook=_pairs)
    except (UnicodeError, ValueError) as exc:
        raise ValueError("INVALID_WEEK_JSON") from exc
    if (not isinstance(obj, dict)
            or set(obj) != {"schema", "synthetic_only", "partition", "monday", "rows"}
            or obj["schema"] != SCHEMA or obj["synthetic_only"] is not True
            or obj["partition"] != partition.fingerprint
            or obj["monday"] != monday or not isinstance(obj["rows"], list)
            or not obj["rows"] or len(obj["rows"]) > 100_000):
        raise ValueError("FOREX_WEEK_CONTEXT_MISMATCH")
    if _canonical(obj) != data[len(MAGIC):]:
        raise ValueError("NONCANONICAL_WEEK_BYTES")
    rows = []
    for r in obj["rows"]:
        if not isinstance(r, dict) or set(r) != _ROW_KEYS:
            raise ValueError("BAD_WEEK_ROW_SCHEMA")
        obs = Observation(
            partition.provider_id, r["stream"], r["endpoint"], r["revision_id"],
            r["raw_sha256"], datetime.fromisoformat(r["obs_known"]),
            datetime.fromisoformat(r["retrieved"]),
            partition.source_timezone_policy, r["license"],
        )
        key = MarketBarKey(
            partition.instrument_version, partition.timeframe,
            datetime.fromisoformat(r["start"]), datetime.fromisoformat(r["end"]),
            partition.calendar_version, partition.aggregation_version,
            partition.side,
        )
        rows.append(MarketBar(
            key, obs, r["revision"], datetime.fromisoformat(r["known"]),
            *(Decimal(r[k]) for k in ("open", "high", "low", "close")),
            BarLifecycle(r["lifecycle"]), BarCoverage(r["coverage"]),
            SourceQuality(r["quality"]),
        ))
    result = tuple(rows)
    _only_fake(partition, result)
    if any(_monday(b) != monday for b in result):
        raise ValueError("MISROUTED_WEEK_DATA")
    CandleSnapshot(partition, result, as_of, "SYNTHETIC_SEALED_WEEK_READ")
    return result


# Compatibility contracts absorbed from the retired parallel-chat-only
# weekly in-memory simulator. The independent #37 encrypted weekly engine uses
# these three types; preserve identical digests and validations without #31.
HEX = re.compile(r"^[a-f0-9]{64}$")

def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()

def _json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False)

@dataclass(frozen=True,slots=True)
class FXWindowRef:
    monday_utc: str
    chunk_name: str
    chunk_sha256: str
    bars: int

    def __post_init__(self):
        if not isinstance(self.monday_utc,str):
            raise ValueError("MONDAY_STORAGE_ID_REQUIRED")
        try:
            d=datetime.fromisoformat(self.monday_utc).date()
        except (ValueError,TypeError) as err:
            raise ValueError("INVALID_UTC_WEEK") from err
        if d.isoformat()!=self.monday_utc or d.weekday()!=0:
            raise ValueError("WINDOW_IS_NOT_MONDAY")
        if not isinstance(self.chunk_sha256,str) or not HEX.fullmatch(self.chunk_sha256):
            raise ValueError("BAD_CHUNK_SHA256")
        if self.chunk_name != f"fx1-w-{self.monday_utc}-{self.chunk_sha256}.fixture":
            raise ValueError("NONCANONICAL_CONTENT_ADDRESS")
        if type(self.bars) is not int or not 1<=self.bars<=100_000:
            raise ValueError("INVALID_WINDOW_BAR_COUNT")


@dataclass(frozen=True,slots=True)
class FXWindowManifest:
    partition_sha256: str
    generation: int
    parent_sha256: str | None
    created_utc: datetime
    refs: tuple[FXWindowRef,...]
    fixture_only: bool = True
    real_drive_calls: int = 0
    may_use_real_market_data: bool = False

    def __post_init__(self):
        if not isinstance(self.partition_sha256,str) or not HEX.fullmatch(self.partition_sha256):
            raise ValueError("PARTITION_HASH_REQUIRED")
        if type(self.generation) is not int or self.generation<1:
            raise ValueError("GENERATION_REQUIRED")
        if (self.generation==1)!=(self.parent_sha256 is None):
            raise ValueError("GENESIS_PARENT_POLICY")
        if self.parent_sha256 is not None and not HEX.fullmatch(self.parent_sha256):
            raise ValueError("PARENT_SHA_REQUIRED")
        ensure_utc(self.created_utc,"created_utc")
        if (not isinstance(self.refs,tuple) or not 0<len(self.refs)<=MAX_WINDOWS
            or any(not isinstance(x,FXWindowRef) for x in self.refs)
            or tuple(x.monday_utc for x in self.refs)!=tuple(sorted({x.monday_utc for x in self.refs}))):
            raise ValueError("STRICT_NONEMPTY_UNIQUE_WINDOWS_REQUIRED")
        if self.fixture_only is not True or self.real_drive_calls!=0 or self.may_use_real_market_data is not False:
            raise PermissionError("FIXTURE_NOT_LIVE_STORAGE")

    @property
    def digest(self) -> str:
        d=asdict(self)
        d["created_utc"]=self.created_utc.isoformat(timespec="microseconds")
        return _sha(_json(d).encode("ascii"))


@dataclass(frozen=True)
class FXWindowSync:
    new_chunk_objects: int
    reused_chunk_objects: int
    new_manifest: bool
    actual_vendor_requests: int = 0
    actual_drive_requests: int = 0
    live_cache_approved: bool = False


@dataclass(frozen=True, slots=True)
class SyntheticEncryptedWindow:
    ref: FXWindowRef
    sealed: SealedSyntheticChunk
    plaintext_sha256: str


class SyntheticSealedWeeklyStore:
    """Fake Drive index and fake head; NO durable CAS, KMS or remote witness."""

    def __init__(self):
        self._objects: dict[str, SyntheticEncryptedWindow] = {}
        self._heads: dict[str, FXWindowManifest] = {}

    @property
    def object_count(self) -> int:
        return len(self._objects)

    def head(self, partition: CachePartition) -> str | None:
        m = self._heads.get(partition.fingerprint)
        return m.digest if m else None

    def _read(self, partition: CachePartition, ref: FXWindowRef, *,
              key: bytes, key_ref: str, as_of: datetime) -> tuple[MarketBar, ...]:
        obj = self._objects.get(ref.chunk_name)
        if obj is None or obj.ref != ref:
            raise ValueError("MISSING_OR_MISMATCHED_ENCRYPTED_WEEK")
        sealed = obj.sealed
        if sealed.partition != partition.fingerprint or sealed.key_ref != key_ref:
            raise ValueError("WRONG_WEEK_CRYPT_CONTEXT")
        raw = unseal_synthetic_fixture(
            sealed, key=key, partition=partition.fingerprint,
            generation=sealed.generation,
            previous_manifest_sha256=sealed.previous_manifest_sha256,
            key_ref=key_ref,
        )
        digest = sha256(raw).hexdigest()
        if digest != obj.plaintext_sha256 or digest != ref.chunk_sha256:
            raise ValueError("WEEK_PLAINTEXT_DIGEST_MISMATCH")
        rows = _unpack(partition, ref.monday_utc, raw, as_of)
        if len(rows) != ref.bars:
            raise ValueError("WEEK_BAR_COUNT_MISMATCH")
        return rows

    def commit(self, snapshot: CandleSnapshot, *, expected_head: str | None,
               key: bytes, key_ref: str,
               fail_after_chunks: bool = False) -> FXWindowSync:
        if not isinstance(snapshot, CandleSnapshot):
            raise TypeError("TYPED_SYNTHETIC_SNAPSHOT_REQUIRED")
        partition = snapshot.partition
        _only_fake(partition, snapshot.closed_bars)
        old = self._heads.get(partition.fingerprint)
        if expected_head != (old.digest if old else None):
            raise ValueError("SIMULATED_STALE_WEEK_WRITER")
        if old is not None and snapshot.checked_at_utc < old.created_utc:
            raise ValueError("NONMONOTONIC_FAKE_COMMIT_CLOCK")
        previous = {r.monday_utc: r for r in old.refs} if old else {}
        groups: dict[str, list[MarketBar]] = {}
        for b in snapshot.closed_bars:
            groups.setdefault(_monday(b), []).append(b)
        if len(groups) > MAX_WINDOWS:
            raise ValueError("TOO_MANY_WEEK_WINDOWS")
        if any(k not in groups for k in previous):
            raise ValueError("UNVERIFIED_WEEK_DELETION")
        generation = old.generation + 1 if old else 1
        parent = old.digest if old else None
        refs = []
        staged: dict[str, SyntheticEncryptedWindow] = {}
        reused = 0
        changed_refs = 0
        for monday, bars in sorted(groups.items()):
            rows = tuple(bars)
            raw = _pack(partition, monday, rows, snapshot.checked_at_utc)
            digest = sha256(raw).hexdigest()
            ref = FXWindowRef(monday, f"fx1-w-{monday}-{digest}.fixture",
                              digest, len(rows))
            if previous.get(monday) == ref:
                if self._read(partition, ref, key=key, key_ref=key_ref,
                              as_of=snapshot.checked_at_utc) != rows:
                    raise ValueError("REUSED_WEEK_ROWS_MISMATCH")
                reused += 1
            else:
                if monday in previous:
                    older_rows = self._read(
                        partition, previous[monday], key=key, key_ref=key_ref,
                        as_of=snapshot.checked_at_utc)
                    older_snapshot = CandleSnapshot(
                        partition, older_rows, snapshot.checked_at_utc,
                        "SYNTHETIC_WEEK_OLDER")
                    merged = reconcile_closed_delta(
                        older_snapshot, rows, snapshot.checked_at_utc,
                        new_source_head_claim="SYNTHETIC_WEEK_REVISION")
                    if merged.snapshot.closed_bars != rows:
                        raise ValueError("UNVERIFIED_INTRA_WEEK_BAR_DELETION")
                changed_refs += 1
                if ref.chunk_name in self._objects:
                    if self._read(partition, ref, key=key, key_ref=key_ref,
                                  as_of=snapshot.checked_at_utc) != rows:
                        raise ValueError("CONTENT_ADDRESS_COLLISION")
                else:
                    sealed = seal_synthetic_fixture(
                        raw, key=key, partition=partition.fingerprint,
                        generation=generation, previous_manifest_sha256=parent,
                        key_ref=key_ref,
                    )
                    staged[ref.chunk_name] = SyntheticEncryptedWindow(ref, sealed, digest)
            refs.append(ref)
        if not changed_refs:
            return FXWindowSync(0, reused, False)
        # All new objects staged prior to head advance. In-memory only.
        self._objects.update(staged)
        if fail_after_chunks:
            raise RuntimeError("SIMULATED_SEALED_WEEK_STAGE_CRASH")
        if self.head(partition) != expected_head:
            raise ValueError("SIMULATED_STALE_WEEK_WRITER")
        manifest = FXWindowManifest(
            partition.fingerprint, generation, parent,
            snapshot.checked_at_utc, tuple(refs),
        )
        self._heads[partition.fingerprint] = manifest
        return FXWindowSync(len(staged), reused, True)

    def select(self, partition: CachePartition, *, pinned_head: str,
               as_of_utc: datetime, key: bytes, key_ref: str,
               window_ids: tuple[str, ...] | None = None,
               minimum_generation: int = 1) -> tuple[MarketBar, ...]:
        ensure_utc(as_of_utc, "as_of_utc")
        manifest = self._heads.get(partition.fingerprint)
        if (manifest is None or manifest.digest != pinned_head
                or type(minimum_generation) is not int
                or minimum_generation < 1
                or manifest.generation < minimum_generation):
            raise ValueError("STALE_OR_UNVERIFIED_SYNTHETIC_WEEK_HEAD")
        refs = {r.monday_utc: r for r in manifest.refs}
        if window_ids is None:
            keys = tuple(sorted(refs))
        elif (not isinstance(window_ids, tuple) or not window_ids
              or len(set(window_ids)) != len(window_ids)
              or any(k not in refs for k in window_ids)):
            raise ValueError("INVALID_WEEK_SELECTION")
        else:
            keys = tuple(sorted(window_ids))
        rows = tuple(b for monday in keys for b in self._read(
            partition, refs[monday], key=key, key_ref=key_ref, as_of=as_of_utc))
        CandleSnapshot(partition, rows, as_of_utc, "SYNTHETIC_WEEK_SELECT")
        return rows
