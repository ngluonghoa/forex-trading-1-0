"""M2/P0.14: synthetic-only encrypted weekly chunk + manifest regression."""
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from forex_trading.cache_core import CachePartition, CandleSnapshot
from forex_trading.market_data import (
    BarCoverage, BarLifecycle, BarSide, MarketBar, MarketBarKey,
    Observation, SourceQuality, Timeframe,
)
from forex_trading.synthetic_sealed_weekly_store import SyntheticSealedWeeklyStore

T = datetime(2026, 1, 5, 12, tzinfo=timezone.utc)
NOW = datetime(2026, 2, 1, tzinfo=timezone.utc)
KEY = bytes(range(32))  # PUBLIC TEST KEY: no confidentiality assertion
KEY_REF = "TESTKEY-01"


def part(pair="EURUSD-fake", side=BarSide.BID, provider="TEST-VENDOR"):
    return CachePartition(provider, "DEMO-PRODUCT", pair, side, Timeframe.M5,
                          "TEST-CALENDAR", "TEST-AGG", "UTC-TEST",
                          "NO-RIGHTS", "SCHEMA1")


def bar(i, *, pair="EURUSD-fake", side=BarSide.BID, provider="TEST-VENDOR",
        rev=1, known=None, close="1.15", endpoint="ONLY_SYNTHETIC"):
    start = T + timedelta(days=i)
    end = start + timedelta(minutes=5)
    at = known or end + timedelta(seconds=1)
    obs = Observation(provider, side.value + "-FAKE", endpoint, f"rev{rev}",
                      str(rev % 10) * 64, at, at, "UTC-TEST", "NO_REAL_LICENSE")
    k = MarketBarKey(pair, Timeframe.M5, start, end,
                     "TEST-CALENDAR", "TEST-AGG", side)
    return MarketBar(k, obs, rev, at, Decimal("1.10"), Decimal("1.20"),
                     Decimal("1.00"), Decimal(close), BarLifecycle.CLOSED,
                     BarCoverage.COMPLETE, SourceQuality.VERIFIED)


def snap(p=None, rows=None, at=NOW):
    return CandleSnapshot(p or part(),
                          rows if rows is not None else tuple(bar(i) for i in range(15)),
                          at, "FAKE-HEAD")


class SealedWeeklyTest(unittest.TestCase):
    def setUp(self):
        self.store = SyntheticSealedWeeklyStore()
        self.p = part()
        self.s = snap()

    def commit(self, s=None, head=None, **extra):
        return self.store.commit(s or self.s, expected_head=head,
                                 key=KEY, key_ref=KEY_REF, **extra)

    def read(self, p=None, **extra):
        p = p or self.p
        return self.store.select(p, pinned_head=self.store.head(p),
                                 as_of_utc=NOW, key=KEY, key_ref=KEY_REF, **extra)

    def test_first_encrypted_three_week_chunks_roundtrip(self):
        result = self.commit()
        self.assertEqual((result.new_chunk_objects, result.reused_chunk_objects,
                          result.new_manifest), (3, 0, True))
        self.assertEqual(self.read(), self.s.closed_bars)
        self.assertEqual((result.actual_drive_requests, result.actual_vendor_requests,
                          result.live_cache_approved), (0, 0, False))
        self.assertEqual(self.store.object_count, 3)

    def test_noop_creates_no_objects_no_manifest(self):
        self.commit()
        h = self.store.head(self.p)
        r = self.commit(head=h)
        self.assertEqual((r.new_chunk_objects, r.reused_chunk_objects,
                          r.new_manifest), (0, 3, False))
        self.assertEqual(self.store.head(self.p), h)

    def test_new_bar_in_existing_week_regenerates_only_one(self):
        self.commit()
        s = snap(rows=self.s.closed_bars + (bar(15),))
        r = self.commit(s, head=self.store.head(self.p))
        self.assertEqual((r.new_chunk_objects, r.reused_chunk_objects), (1, 2))
        self.assertEqual(self.read(), s.closed_bars)

    def test_new_week_adds_only_one(self):
        self.commit()
        s = snap(rows=self.s.closed_bars + (bar(21),))
        r = self.commit(s, head=self.store.head(self.p))
        self.assertEqual((r.new_chunk_objects, r.reused_chunk_objects), (1, 3))
        self.assertEqual(self.store.object_count, 4)

    def test_revised_old_week_preserves_others(self):
        self.commit()
        rows = tuple(bar(i, rev=2, close="1.16",
                         known=NOW - timedelta(hours=2)) if i == 2
                     else bar(i) for i in range(15))
        r = self.commit(snap(rows=rows), head=self.store.head(self.p))
        self.assertEqual((r.new_chunk_objects, r.reused_chunk_objects), (1, 2))
        self.assertEqual(self.read(), rows)

    def test_select_one_week_only(self):
        self.commit()
        self.assertEqual(self.read(window_ids=("2026-01-12",)),
                         self.s.closed_bars[7:14])

    def test_different_pair_side_isolation(self):
        self.commit()
        other = part(pair="GBPUSD-fake", side=BarSide.ASK)
        rows = tuple(bar(i, pair="GBPUSD-fake", side=BarSide.ASK)
                     for i in range(15))
        self.store.commit(snap(other, rows), expected_head=None,
                          key=KEY, key_ref=KEY_REF)
        self.assertNotEqual(self.store.head(self.p), self.store.head(other))
        self.assertEqual(self.read(other), rows)

    def test_reject_wrong_key(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.store.select(self.p, pinned_head=self.store.head(self.p),
                              as_of_utc=NOW, key=b"Z" * 32, key_ref=KEY_REF)

    def test_reject_wrong_key_reference(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.store.select(self.p, pinned_head=self.store.head(self.p),
                              as_of_utc=NOW, key=KEY, key_ref="OTHKEY-01")

    def test_reject_tampered_encrypted_envelope(self):
        self.commit()
        name = next(iter(self.store._objects))
        obj = self.store._objects[name]
        changed = bytes([obj.sealed.ciphertext_with_tag[0] ^ 1]) + obj.sealed.ciphertext_with_tag[1:]
        self.store._objects[name] = replace(
            obj, sealed=replace(obj.sealed, ciphertext_with_tag=changed))
        with self.assertRaises(ValueError):
            self.read()

    def test_reject_wrong_pin_or_generation_floor(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.store.select(self.p, pinned_head="f" * 64,
                              as_of_utc=NOW, key=KEY, key_ref=KEY_REF)
        with self.assertRaises(ValueError):
            self.read(minimum_generation=2)

    def test_reject_stale_writer(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.commit(head=None)

    def test_reject_unverified_week_deletion(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.commit(snap(rows=self.s.closed_bars[7:]),
                        head=self.store.head(self.p))

    def test_stage_crash_leaves_no_head_and_retry_reuses_orphans(self):
        with self.assertRaises(RuntimeError):
            self.commit(fail_after_chunks=True)
        self.assertIsNone(self.store.head(self.p))
        self.assertEqual(self.store.object_count, 3)
        r = self.commit()
        self.assertTrue(r.new_manifest)
        self.assertEqual(r.new_chunk_objects, 0)
        self.assertEqual(self.read(), self.s.closed_bars)

    def test_corrupt_orphan_blocks_commit(self):
        with self.assertRaises(RuntimeError):
            self.commit(fail_after_chunks=True)
        name = next(iter(self.store._objects))
        obj = self.store._objects[name]
        self.store._objects[name] = replace(obj, plaintext_sha256="0" * 64)
        with self.assertRaises(ValueError):
            self.commit()

    def test_real_vendor_endpoint_forbidden(self):
        rows = self.s.closed_bars[:-1] + (bar(14, endpoint="LIVE_API"),)
        with self.assertRaises(PermissionError):
            self.commit(snap(rows=rows))

    def test_rights_claim_cannot_unlock_fixture_store(self):
        p = replace(self.p, rights_policy_ref="CLAIMED_LICENSE")
        with self.assertRaises(PermissionError):
            self.commit(snap(p=p))

    def test_future_known_correction_blocked(self):
        rows = self.s.closed_bars[:-1] + (
            bar(14, rev=2, known=NOW + timedelta(hours=1)),)
        with self.assertRaises(ValueError):
            snap(rows=rows)

    def test_no_direct_drive_or_live_trading_flag(self):
        self.commit()
        self.assertNotIn("drive", self.store.__dict__)
        self.assertNotIn("broker", self.store.__dict__)


if __name__ == "__main__":
    unittest.main()
