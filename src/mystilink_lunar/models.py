# -*- coding: utf-8 -*-
"""Ganzhi models and rule enums (alpha.3)."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from mystilink_lunar.constants import BRANCHES, STEMS, ZODIAC_EN, ZODIAC_ZH

YearBoundary = Literal["chunjie", "lichun_day", "lichun_exact"]
MonthBoundary = Literal["jie_exact", "jie_day", "lunar_month"]
DayBoundary = Literal["midnight", "zi_start"]
HourSystem = Literal["double_hour"]


@dataclass(frozen=True)
class LunarDate:
    """Civil lunar date components."""

    year: int
    month: int
    day: int
    is_leap_month: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "is_leap_month": self.is_leap_month,
        }


@dataclass(frozen=True)
class SolarDate:
    """Gregorian civil date (no time)."""

    year: int
    month: int
    day: int

    def to_dict(self) -> Dict[str, Any]:
        return {"year": self.year, "month": self.month, "day": self.day}


@dataclass(frozen=True)
class Ganzhi:
    """One stem-branch pair; store indices, expose glyphs via properties."""

    stem_index: int
    branch_index: int

    def __post_init__(self) -> None:
        if not 0 <= self.stem_index <= 9:
            raise ValueError(f"stem_index out of range: {self.stem_index}")
        if not 0 <= self.branch_index <= 11:
            raise ValueError(f"branch_index out of range: {self.branch_index}")

    @property
    def stem(self) -> str:
        return STEMS[self.stem_index]

    @property
    def branch(self) -> str:
        return BRANCHES[self.branch_index]

    @property
    def text(self) -> str:
        return f"{self.stem}{self.branch}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stem_index": self.stem_index,
            "branch_index": self.branch_index,
            "stem": self.stem,
            "branch": self.branch,
            "text": self.text,
        }


@dataclass(frozen=True)
class Zodiac:
    """Animal year keyed by earthly-branch index."""

    branch_index: int

    def __post_init__(self) -> None:
        if not 0 <= self.branch_index <= 11:
            raise ValueError(f"branch_index out of range: {self.branch_index}")

    @property
    def id(self) -> str:
        return ZODIAC_EN[self.branch_index]

    @property
    def chinese(self) -> str:
        return ZODIAC_ZH[self.branch_index]

    @property
    def branch(self) -> str:
        return BRANCHES[self.branch_index]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "chinese": self.chinese,
            "branch": self.branch,
            "branch_index": self.branch_index,
        }


@dataclass(frozen=True)
class SolarTerm:
    """One of the 24 solar terms at an exact local instant."""

    index: int
    id: str
    name: str
    chinese_name: str
    solar_longitude: float
    datetime: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "id": self.id,
            "name": self.name,
            "chinese_name": self.chinese_name,
            "solar_longitude": self.solar_longitude,
            "datetime": self.datetime.isoformat(),
        }


@dataclass(frozen=True)
class GanzhiRules:
    """Explicit sexagenary boundary rules for four pillars."""

    year_boundary: YearBoundary = "chunjie"
    month_boundary: MonthBoundary = "lunar_month"
    day_boundary: DayBoundary = "midnight"
    hour_system: HourSystem = "double_hour"

    @classmethod
    def lunar_calendar(cls) -> GanzhiRules:
        """Calendar-oriented defaults: lunar new year and lunar months."""
        return cls(
            year_boundary="chunjie",
            month_boundary="lunar_month",
            day_boundary="midnight",
            hour_system="double_hour",
        )

    @classmethod
    def bazi_default(cls) -> GanzhiRules:
        """BaZi-oriented defaults: Li Chun exact, jie exact, day rolls at 23:00."""
        return cls(
            year_boundary="lichun_exact",
            month_boundary="jie_exact",
            day_boundary="zi_start",
            hour_system="double_hour",
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GanzhiPillars:
    """Four pillars: year / month / day / hour."""

    year: Ganzhi
    month: Ganzhi
    day: Ganzhi
    hour: Ganzhi

    def to_dict(self) -> Dict[str, Any]:
        return {
            "year": self.year.to_dict(),
            "month": self.month.to_dict(),
            "day": self.day.to_dict(),
            "hour": self.hour.to_dict(),
        }


@dataclass(frozen=True)
class PillarTrace:
    """Deterministic rule trace for one pillar (not LLM text)."""

    value: str
    stem_index: int
    branch_index: int
    boundary: str
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "stem_index": self.stem_index,
            "branch_index": self.branch_index,
            "boundary": self.boundary,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class GanzhiTrace:
    """Deterministic rule traces for all four pillars."""

    year: PillarTrace
    month: PillarTrace
    day: PillarTrace
    hour: PillarTrace
    rules: GanzhiRules

    def to_dict(self) -> Dict[str, Any]:
        return {
            "year": self.year.to_dict(),
            "month": self.month.to_dict(),
            "day": self.day.to_dict(),
            "hour": self.hour.to_dict(),
            "rules": self.rules.to_dict(),
        }


@dataclass(frozen=True)
class CalendarSnapshot:
    """Structured conversion result suitable for agents and engines."""

    instant: datetime
    timezone: str
    solar: SolarDate
    lunar: LunarDate
    zodiac: Zodiac
    ganzhi: GanzhiPillars
    rules: GanzhiRules
    provider: str
    previous_solar_term: Optional[SolarTerm] = None
    next_solar_term: Optional[SolarTerm] = None

    @property
    def year_ganzhi(self) -> Ganzhi:
        return self.ganzhi.year

    def to_dict(self) -> Dict[str, Any]:
        return {
            "solar": {
                "datetime": self.instant.isoformat(),
                "timezone": self.timezone,
                "year": self.solar.year,
                "month": self.solar.month,
                "day": self.solar.day,
            },
            "lunar": self.lunar.to_dict(),
            "ganzhi": self.ganzhi.to_dict(),
            "zodiac": self.zodiac.to_dict(),
            "rules": self.rules.to_dict(),
            "provider": self.provider,
            "solar_term": {
                "previous": (
                    self.previous_solar_term.to_dict()
                    if self.previous_solar_term is not None
                    else None
                ),
                "next": (
                    self.next_solar_term.to_dict()
                    if self.next_solar_term is not None
                    else None
                ),
            },
        }
