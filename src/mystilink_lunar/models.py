# -*- coding: utf-8 -*-
"""Immutable calendar data models."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Literal

from mystilink_lunar.constants import BRANCHES, STEMS, ZODIAC_EN, ZODIAC_ZH

YearBoundary = Literal["chunjie", "lichun_day", "lichun_exact"]


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
class GanzhiRules:
    """Explicit sexagenary boundary rules (more pillars in later alphas)."""

    year_boundary: YearBoundary = "chunjie"

    @classmethod
    def lunar_calendar(cls) -> GanzhiRules:
        """Calendar-oriented defaults: lunar new year for year pillar/zodiac."""
        return cls(year_boundary="chunjie")

    @classmethod
    def bazi_default(cls) -> GanzhiRules:
        """BaZi-oriented defaults (lichun exact; full pillars later)."""
        return cls(year_boundary="lichun_exact")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalendarSnapshot:
    """Structured conversion result suitable for agents and engines."""

    instant: datetime
    timezone: str
    solar: SolarDate
    lunar: LunarDate
    zodiac: Zodiac
    year_ganzhi: Ganzhi
    rules: GanzhiRules
    provider: str

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
            "ganzhi": {
                "year": self.year_ganzhi.to_dict(),
            },
            "zodiac": self.zodiac.to_dict(),
            "rules": self.rules.to_dict(),
            "provider": self.provider,
            "solar_term": None,
        }
