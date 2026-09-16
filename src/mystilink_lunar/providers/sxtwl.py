# -*- coding: utf-8 -*-
"""sxtwl-backed calendar provider (not part of the public API surface)."""
from __future__ import annotations

from datetime import datetime
from typing import List, Tuple
from zoneinfo import ZoneInfo

from mystilink_lunar.exceptions import (
    DateOutOfRangeError,
    InvalidLunarDateError,
    ProviderError,
    SolarTermNotFoundError,
)
from mystilink_lunar.models import LunarDate, SolarDate
from mystilink_lunar.timezone import resolve_zone

# Practical validation window for alpha; sxtwl itself supports a wider range.
_MIN_YEAR = 1900
_MAX_YEAR = 2100

# 寿星 / sxtwl JD2DD wall clock is China Standard Time (UTC+8).
_SXTWL_WALL_TZ = ZoneInfo("Asia/Shanghai")


class SxtwlProvider:
    """Adapter around the sxtwl PyPI package."""

    name = "sxtwl"

    def __init__(self) -> None:
        try:
            import sxtwl  # noqa: F401
        except ImportError as exc:
            raise ProviderError(
                "sxtwl is required for the default provider; install mystilink-lunar"
            ) from exc

    def solar_to_lunar(self, solar: SolarDate) -> LunarDate:
        self._check_solar(solar)
        import sxtwl

        try:
            day = sxtwl.fromSolar(solar.year, solar.month, solar.day)
        except Exception as exc:  # noqa: BLE001 — SWIG raises varied types
            raise ProviderError(f"sxtwl.fromSolar failed: {exc}") from exc
        return LunarDate(
            year=int(day.getLunarYear()),
            month=int(day.getLunarMonth()),
            day=int(day.getLunarDay()),
            is_leap_month=bool(day.isLunarLeap()),
        )

    def lunar_to_solar(self, lunar: LunarDate) -> SolarDate:
        if not 1 <= lunar.month <= 12:
            raise InvalidLunarDateError(f"lunar month out of range: {lunar.month}")
        if not 1 <= lunar.day <= 30:
            raise InvalidLunarDateError(f"lunar day out of range: {lunar.day}")
        if not _MIN_YEAR <= lunar.year <= _MAX_YEAR:
            raise DateOutOfRangeError(
                f"lunar year {lunar.year} outside supported range {_MIN_YEAR}-{_MAX_YEAR}"
            )
        import sxtwl

        try:
            day = sxtwl.fromLunar(
                lunar.year, lunar.month, lunar.day, bool(lunar.is_leap_month)
            )
        except Exception as exc:  # noqa: BLE001
            raise InvalidLunarDateError(
                f"invalid lunar date {lunar.year}-{lunar.month}-{lunar.day} "
                f"leap={lunar.is_leap_month}: {exc}"
            ) from exc
        return SolarDate(
            year=int(day.getSolarYear()),
            month=int(day.getSolarMonth()),
            day=int(day.getSolarDay()),
        )

    def solar_term_events(
        self, year: int
    ) -> List[Tuple[int, datetime]]:
        """
        Return (jq_index, aware datetime in Asia/Shanghai) for terms listed by
        sxtwl.getJieQiByYear(year). Includes spill from adjacent years.
        """
        if not _MIN_YEAR <= year <= _MAX_YEAR:
            raise DateOutOfRangeError(
                f"year {year} outside supported range {_MIN_YEAR}-{_MAX_YEAR}"
            )
        import sxtwl

        out: List[Tuple[int, datetime]] = []
        try:
            for info in sxtwl.getJieQiByYear(year):
                out.append((int(info.jqIndex), self._jd_to_shanghai(float(info.jd))))
        except Exception as exc:  # noqa: BLE001
            raise ProviderError(f"sxtwl.getJieQiByYear({year}) failed: {exc}") from exc
        return out

    def solar_term_instant(
        self, index: int, year: int, *, timezone: str
    ) -> datetime:
        """Exact instant of solar term `index` whose civil year (CST) equals `year`."""
        if not 0 <= index <= 23:
            raise SolarTermNotFoundError(f"solar term index out of range: {index}")
        tz = resolve_zone(timezone)
        # Query year and year-1 so January terms of `year` are covered.
        candidates: List[datetime] = []
        for y in (year - 1, year, year + 1):
            if not _MIN_YEAR <= y <= _MAX_YEAR:
                continue
            for jq_index, shanghai in self.solar_term_events(y):
                if jq_index == index and shanghai.year == year:
                    candidates.append(shanghai.astimezone(tz))
        # Deduplicate identical instants from overlapping year queries
        uniq: List[datetime] = []
        seen: set[str] = set()
        for dt in candidates:
            key = dt.isoformat()
            if key not in seen:
                seen.add(key)
                uniq.append(dt)
        if not uniq:
            raise SolarTermNotFoundError(
                f"solar term index={index} not found for year {year}"
            )
        if len(uniq) > 1:
            # Prefer the earliest occurrence in that civil year
            uniq.sort()
        return uniq[0]

    def _jd_to_shanghai(self, jd: float) -> datetime:
        import sxtwl

        t = sxtwl.JD2DD(jd)
        year = int(t.Y)
        month = int(t.M)
        day = int(t.D)
        hour = int(t.h)
        minute = int(t.m)
        sec_f = float(t.s)
        second = int(sec_f)
        micro = int(round((sec_f - second) * 1_000_000))
        if micro >= 1_000_000:
            second += 1
            micro -= 1_000_000
        if second >= 60:
            # Rare float rounding edge; push via replace after construct
            second = 59
            micro = 999999
        return datetime(
            year, month, day, hour, minute, second, micro, tzinfo=_SXTWL_WALL_TZ
        )

    def _check_solar(self, solar: SolarDate) -> None:
        if not _MIN_YEAR <= solar.year <= _MAX_YEAR:
            raise DateOutOfRangeError(
                f"solar year {solar.year} outside supported range {_MIN_YEAR}-{_MAX_YEAR}"
            )
        if not 1 <= solar.month <= 12:
            raise DateOutOfRangeError(f"solar month out of range: {solar.month}")
        if not 1 <= solar.day <= 31:
            raise DateOutOfRangeError(f"solar day out of range: {solar.day}")
