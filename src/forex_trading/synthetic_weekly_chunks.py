"""M2/P0.12 — synthetic-only per-week immutable Forex cache window reference.

Window objects contain typed closed BID/ASK MarketBar fixtures in MEMORY, not
serialized Google Drive bytes. No licensed vendor quotes, broker execution,
cloud API, background polling, source permission or external witness.
UTC Mondays group STORAGE ONLY: NEVER infer DST/session/rollover from them.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from hashlib import sha256
import json
import re

from .cache_core import CachePartition, CandleSnapshot
from .market_data import MarketBar
from .quotes import ensure_utc

HEX = re.compile(r"^[a-f0-9]{64}$")
MAX_WINDOWS = 256


def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def _json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False)


def _monday(bar: MarketBar) -> str:
    d=bar.key.bar_start_utc.date()
    return (d-timedelta(days=d.weekday())).isoformat()


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


class SyntheticFXWeeklyIndex:
    """Two-level immutable per-week fake cache with local generation tracking.

    All row tuples remain inside this process and are independently revalidated
    against the existing typed CandleSnapshot contract on read. The active
    pointer and hash history are NOT an authenticated monotonic off-host witness.
    """

    def __init__(self):
        self._chunks: dict[str,tuple[MarketBar,...]]={}
        self._manifests: dict[str,FXWindowManifest]={}
        self._history: dict[str,list[str]]={}
        self._head: dict[str,str]={}

    @property
    def object_count(self):
        return len(self._chunks)

    def head(self, partition: CachePartition) -> str | None:
        if not isinstance(partition,CachePartition):
            raise TypeError("CACHE_PARTITION_REQUIRED")
        return self._head.get(partition.fingerprint)

    def _chain(self, partition: CachePartition) -> tuple[FXWindowManifest,...]:
        sha=partition.fingerprint
        ids=self._history.get(sha,[])
        if not ids:
            if sha in self._head:
                raise ValueError("POINTER_WITHOUT_HISTORY")
            return ()
        if self._head.get(sha)!=ids[-1]:
            raise ValueError("ACTIVE_POINTER_NOT_WITNESSED_IN_FAKE_HISTORY")
        parent=None
        records=[]
        for i,digest in enumerate(ids,1):
            m=self._manifests.get(digest)
            if (m is None or m.digest!=digest or m.partition_sha256!=sha or
                    m.generation!=i or m.parent_sha256!=parent):
                raise ValueError("BROKEN_FX_WINDOW_MANIFEST_CHAIN")
            records.append(m)
            parent=digest
        return tuple(records)

    @staticmethod
    def _digest(partition: CachePartition, rows: tuple[MarketBar,...], checked_at_utc: datetime) -> str:
        return CandleSnapshot(partition,rows,checked_at_utc,"SYNTHETIC_WINDOW_HEAD").fingerprint

    def _verify(self, partition: CachePartition, ref: FXWindowRef, as_of: datetime) -> tuple[MarketBar,...]:
        bars=self._chunks.get(ref.chunk_name)
        if bars is None or len(bars)!=ref.bars or not all(_monday(b)==ref.monday_utc for b in bars):
            raise ValueError("MISSING_OR_MISROUTED_FX_WINDOW")
        if self._digest(partition,bars,as_of)!=ref.chunk_sha256:
            raise ValueError("CORRUPT_FX_WINDOW_FIXTURE_ROWS")
        return bars

    def commit(self, snapshot: CandleSnapshot, *, expected_head: str | None,
               fail_after_chunks: bool = False) -> FXWindowSync:
        if not isinstance(snapshot,CandleSnapshot):
            raise TypeError("QUALIFIED_SYNTHETIC_SNAPSHOT_REQUIRED")
        if not snapshot.closed_bars or type(fail_after_chunks) is not bool:
            raise ValueError("NONEMPTY_TYPED_FAKE_HISTORY_REQUIRED")
        chain=self._chain(snapshot.partition)
        if expected_head!=self.head(snapshot.partition):
            raise ValueError("STALE_SYNTHETIC_FX_WRITER")
        if expected_head is not None and (not isinstance(expected_head,str) or not HEX.fullmatch(expected_head)):
            raise ValueError("INVALID_EXPECTED_HEAD")
        older=chain[-1] if chain else None
        previous={x.monday_utc:x for x in older.refs} if older else {}
        groups:dict[str,list[MarketBar]]={}
        for b in snapshot.closed_bars:
            groups.setdefault(_monday(b),[]).append(b)
        if len(groups)>MAX_WINDOWS:
            raise ValueError("TOO_MANY_WINDOWS")
        if any(k not in groups for k in previous):
            raise ValueError("UNVERIFIED_FULL_WINDOW_DELETION_BLOCKED")
        refs=[]
        added=reused=0
        for monday,rows in sorted(groups.items()):
            typed=tuple(rows)
            digest=self._digest(snapshot.partition,typed,snapshot.checked_at_utc)
            ref=FXWindowRef(monday,f"fx1-w-{monday}-{digest}.fixture",digest,len(rows))
            if previous.get(monday)==ref:
                self._verify(snapshot.partition,ref,snapshot.checked_at_utc)
                reused+=1
            else:
                if ref.chunk_name in self._chunks and self._chunks[ref.chunk_name]!=typed:
                    raise ValueError("CONTENT_ADDRESS_COLLISION")
                self._chunks.setdefault(ref.chunk_name,typed)
                added+=1
            refs.append(ref)
        if not added:
            return FXWindowSync(0,reused,False)
        if fail_after_chunks:
            raise RuntimeError("SIMULATED_CHUNK_STAGE_CRASH")
        for ref in refs:
            self._verify(snapshot.partition,ref,snapshot.checked_at_utc)
        m=FXWindowManifest(snapshot.partition.fingerprint,len(chain)+1,
                           older.digest if older else None,snapshot.checked_at_utc,tuple(refs))
        self._manifests[m.digest]=m
        self._history.setdefault(snapshot.partition.fingerprint,[]).append(m.digest)
        self._head[snapshot.partition.fingerprint]=m.digest
        return FXWindowSync(added,reused,True)

    def select(self, partition: CachePartition, *, pinned_head: str,
               as_of_utc: datetime, window_ids: tuple[str,...] | None = None,
               minimum_generation: int = 1) -> tuple[MarketBar,...]:
        if not isinstance(pinned_head,str) or not HEX.fullmatch(pinned_head):
            raise ValueError("PINNED_HEAD_REQUIRED")
        ensure_utc(as_of_utc,"as_of_utc")
        if type(minimum_generation) is not int or minimum_generation<1:
            raise ValueError("INVALID_GENERATION_FLOOR")
        chain=self._chain(partition)
        if not chain or chain[-1].digest!=pinned_head or chain[-1].generation<minimum_generation:
            raise ValueError("STALE_OR_ROLLBACK_FX_HEAD")
        manifest=chain[-1]
        available={ref.monday_utc:ref for ref in manifest.refs}
        if window_ids is None:
            keys=tuple(sorted(available))
        else:
            if (not isinstance(window_ids,tuple) or not window_ids
                    or len(set(window_ids))!=len(window_ids)
                    or any(k not in available for k in window_ids)):
                raise ValueError("UNKNOWN_OR_DUPLICATE_WINDOW_SELECTION")
            keys=tuple(sorted(window_ids))
        rows=tuple(b for k in keys for b in self._verify(partition,available[k],as_of_utc))
        # Verify merged ordering and exact partition/quality/clock before returning.
        CandleSnapshot(partition,rows,as_of_utc,"SYNTHETIC_WINDOW_READBACK")
        return rows

    def reconstruct(self, partition: CachePartition, *, pinned_head: str,
                    as_of_utc: datetime, source_head_claim: str) -> CandleSnapshot:
        return CandleSnapshot(partition,self.select(partition,pinned_head=pinned_head,
               as_of_utc=as_of_utc),as_of_utc,source_head_claim)

    def corrupt_latest_for_test(self, partition: CachePartition):
        latest=self._chain(partition)[-1]
        ref=latest.refs[-1]
        del self._chunks[ref.chunk_name]


def require_approved_forex_storage(*_args: object,**_kwargs: object)->None:
    raise PermissionError("No licensed real Forex storage/Drive adapter/production lease")
