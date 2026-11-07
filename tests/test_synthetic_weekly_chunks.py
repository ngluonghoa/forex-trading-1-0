"""M2/P0.12 synthetic-only windowed FX per-pair BID/ASK immutable storage."""
import unittest
from datetime import datetime,timedelta,timezone
from decimal import Decimal

from forex_trading.cache_core import CachePartition,CandleSnapshot
from forex_trading.market_data import (
    MarketBar,MarketBarKey,Observation,BarSide,Timeframe,BarCoverage,
    BarLifecycle,SourceQuality,
)
from forex_trading.synthetic_weekly_chunks import (
    SyntheticFXWeeklyIndex, FXWindowRef, require_approved_forex_storage,
)

T=datetime(2026,1,5,12,tzinfo=timezone.utc)
NOW=datetime(2026,2,1,0,tzinfo=timezone.utc)
def part(*,pair="EURUSD-fake",side=BarSide.BID,provider="TEST-VENDOR"):
    return CachePartition(provider,"DEMO-PRODUCT",pair,side,Timeframe.M5,
                          "TEST-CALENDAR","TEST-AGG","UTC-TEST","NO-RIGHTS","SCHEMA1")

def bar(i,*,pair="EURUSD-fake",side=BarSide.BID,provider="TEST-VENDOR",
        rev=1,known=None,close="1.15",coverage=BarCoverage.COMPLETE):
    start=T+timedelta(days=i)
    end=start+timedelta(minutes=5)
    at=known or (end+timedelta(seconds=1))
    obs=Observation(provider,side.value+"-FAKE", "ONLY_SYNTHETIC",f"rev{rev}",
                    f"{rev%10}"*64,at,at,"UTC-TEST","NO_REAL_LICENSE")
    key=MarketBarKey(pair,Timeframe.M5,start,end,"TEST-CALENDAR","TEST-AGG",side)
    return MarketBar(key,obs,rev,at,Decimal("1.10"),Decimal("1.20"),
                     Decimal("1.00"),Decimal(close),BarLifecycle.CLOSED,
                     coverage,SourceQuality.VERIFIED)

def snap(p=None,rows=None,at=NOW,head="HEAD-FIXTURE-1"):
    return CandleSnapshot(p or part(), rows if rows is not None else tuple(bar(i) for i in range(15)),
                          at,head)

class FXWeeklyTest(unittest.TestCase):
    def setUp(self):
        self.cloud=SyntheticFXWeeklyIndex()
        self.p=part()
        self.s=snap()

    def commit(self,s=None,head=None,**kw):
        return self.cloud.commit(s or self.s,expected_head=head,**kw)

    def test_initial_three_weeks(self):
        r=self.commit()
        self.assertEqual((r.new_chunk_objects,r.reused_chunk_objects,r.new_manifest),(3,0,True))
        self.assertEqual(self.cloud.object_count,3)
        self.assertEqual(self.cloud.reconstruct(self.p,pinned_head=self.cloud.head(self.p),
            as_of_utc=NOW,source_head_claim="AFTER_REOPEN").closed_bars,self.s.closed_bars)

    def test_noop_no_new_chunks(self):
        self.commit()
        head=self.cloud.head(self.p)
        r=self.commit(head=head)
        self.assertEqual((r.new_chunk_objects,r.reused_chunk_objects,r.new_manifest),(0,3,False))
        self.assertEqual((r.actual_vendor_requests,r.actual_drive_requests,r.live_cache_approved),
                         (0,0,False))
        self.assertEqual(self.cloud.head(self.p),head)

    def test_append_into_current_week(self):
        self.commit()
        s=snap(rows=self.s.closed_bars+(bar(15),))
        r=self.commit(s,head=self.cloud.head(self.p))
        self.assertEqual((r.new_chunk_objects,r.reused_chunk_objects),(1,2))

    def test_new_week_only_one_new_chunk(self):
        self.commit()
        s=snap(rows=self.s.closed_bars+(bar(21),))
        r=self.commit(s,head=self.cloud.head(self.p))
        self.assertEqual((r.new_chunk_objects,r.reused_chunk_objects),(1,3))

    def test_old_revision_changes_only_week_one(self):
        self.commit()
        previous=self.cloud.head(self.p)
        rows=tuple(bar(i,rev=2,known=NOW-timedelta(hours=2),close="1.16")
                   if i==2 else bar(i) for i in range(15))
        r=self.commit(snap(rows=rows),head=previous)
        self.assertEqual((r.new_chunk_objects,r.reused_chunk_objects),(1,2))
        self.assertEqual(self.cloud.object_count,4)
        m=self.cloud._manifests[self.cloud.head(self.p)]
        self.assertEqual((m.generation,m.parent_sha256),(2,previous))
        self.assertEqual(self.cloud.reconstruct(self.p,pinned_head=self.cloud.head(self.p),
             as_of_utc=NOW,source_head_claim="TEST").closed_bars,rows)

    def test_select_one_window_only(self):
        self.commit()
        q=self.cloud.select(self.p,pinned_head=self.cloud.head(self.p),
                            as_of_utc=NOW,window_ids=("2026-01-12",))
        self.assertEqual(q,self.s.closed_bars[7:14])

    def test_corrupt_unselected_window_allows_selected_only(self):
        self.commit()
        h=self.cloud.head(self.p)
        self.cloud.corrupt_latest_for_test(self.p)
        self.assertEqual(self.cloud.select(self.p,pinned_head=h,as_of_utc=NOW,
                            window_ids=("2026-01-05",)),self.s.closed_bars[:7])
        with self.assertRaises(ValueError):
            self.cloud.select(self.p,pinned_head=h,as_of_utc=NOW)

    def test_corrupt_noop_denied(self):
        self.commit()
        self.cloud.corrupt_latest_for_test(self.p)
        with self.assertRaises(ValueError):
            self.commit(head=self.cloud.head(self.p))

    def test_wrong_pin_denied(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.cloud.select(self.p,pinned_head="0"*64,as_of_utc=NOW)

    def test_stale_writer_denied(self):
        self.commit()
        with self.assertRaises(ValueError):self.commit(head=None)

    def test_rollback_generation_floor_denied(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.cloud.select(self.p,pinned_head=self.cloud.head(self.p),
                              as_of_utc=NOW,minimum_generation=2)

    def test_old_week_missing_denied(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.commit(snap(rows=self.s.closed_bars[7:]),head=self.cloud.head(self.p))

    def test_stage_failure_does_not_update_head(self):
        with self.assertRaises(RuntimeError):
            self.commit(fail_after_chunks=True)
        self.assertEqual(self.cloud.object_count,3)
        self.assertIsNone(self.cloud.head(self.p))
        self.assertEqual(self.commit().new_chunk_objects,3)

    def test_bid_and_ask_isolation(self):
        self.commit()
        p2=part(side=BarSide.ASK)
        s2=snap(p=p2,rows=tuple(bar(i,side=BarSide.ASK) for i in range(15)))
        self.cloud.commit(s2,expected_head=None)
        self.assertNotEqual(self.cloud.head(self.p),self.cloud.head(p2))

    def test_pair_isolation(self):
        self.commit()
        p2=part(pair="GBPUSD-fake")
        s2=snap(p=p2,rows=tuple(bar(i,pair="GBPUSD-fake") for i in range(15)))
        self.cloud.commit(s2,expected_head=None)
        old=self.cloud.head(p2)
        self.commit(snap(rows=self.s.closed_bars+(bar(15),)),head=self.cloud.head(self.p))
        self.assertEqual(self.cloud.head(p2),old)

    def test_wrong_side_partition_rejected(self):
        with self.assertRaises(ValueError):
            self.commit(snap(p=part(side=BarSide.ASK),rows=self.s.closed_bars))

    def test_future_known_bar_denied(self):
        rows=self.s.closed_bars[:-1]+(bar(14,rev=2,known=NOW+timedelta(days=1)),)
        with self.assertRaises(ValueError):snap(rows=rows)

    def test_insufficient_quality_denied(self):
        rows=self.s.closed_bars[:-1]+(bar(14,coverage=BarCoverage.PARTIAL),)
        with self.assertRaises(ValueError):snap(rows=rows)

    def test_unknown_window_denied(self):
        self.commit()
        with self.assertRaises(ValueError):
            self.cloud.select(self.p,pinned_head=self.cloud.head(self.p),
                              as_of_utc=NOW,window_ids=("2027-01-04",))

    def test_monday_validation_denied(self):
        with self.assertRaises(ValueError):
            FXWindowRef("2026-01-06","bogus","0"*64,1)

    def test_no_real_drive_or_licence(self):
        with self.assertRaises(PermissionError):require_approved_forex_storage()

if __name__=="__main__":
    unittest.main()
