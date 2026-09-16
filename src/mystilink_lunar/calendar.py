# -*- coding: utf-8 -*-
"""LunarCalendar facade."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union, overload

from mystilink_lunar.ganzhi import compute_pillars
from mystilink_lunar.lunar import lunar_to_solar, solar_to_lunar
from mystilink_lunar.models import (
    CalendarSnapshot,
    Ganzhi,
    GanzhiPillars,
    GanzhiRules,
    GanzhiTrace,
    LunarDate,
    SolarDate,
    SolarTerm,
    Zodiac,
)
from mystilink_lunar.providers import CalendarProvider, default_provider
from mystilink_lunar.solar_terms import adjacent_solar_terms
from mystilink_lunar.timezone import build_aware_datetime, civil_date_in_zone, require_aware


class LunarCalendar:
    """
    Timezone-aware Chinese lunar calendar snapshot.

    Alpha.3: solar↔lunar, solar terms, four pillars with explicit rules + explain.
    """

    def __init__(
        self,
        instant: datetime,
        *,
        rules: Optional[GanzhiRules] = None,
        provider: Optional[CalendarProvider] = None,
    ) -> None:
        self._instant = require_aware(instant)
        self._rules = rules or GanzhiRules.lunar_calendar()
        self._provider = provider or default_provider()
        civil = civil_date_in_zone(self._instant)
        self._solar = SolarDate(civil.year, civil.month, civil.day)
        self._lunar = solar_to_lunar(self._solar, provider=self._provider)
        pillars, zodiac, _trace = compute_pillars(
            self._instant,
            self._lunar,
            rules=self._rules,
            provider=self._provider,
        )
        self._pillars = pillars
        self._zodiac = zodiac
        prev, nxt = adjacent_solar_terms(self._instant, provider=self._provider)
        self._previous_solar_term = prev
        self._next_solar_term = nxt

    @classmethod
    def from_solar(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        *,
        timezone: str,
        rules: Optional[GanzhiRules] = None,
        provider: Optional[CalendarProvider] = None,
    ) -> LunarCalendar:
        instant = build_aware_datetime(
            year, month, day, hour, minute, second, timezone=timezone
        )
        return cls(instant, rules=rules, provider=provider)

    @classmethod
    def from_lunar(
        cls,
        year: int,
        month: int,
        day: int,
        *,
        is_leap_month: bool = False,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        timezone: str,
        rules: Optional[GanzhiRules] = None,
        provider: Optional[CalendarProvider] = None,
    ) -> LunarCalendar:
        eng = provider or default_provider()
        solar = lunar_to_solar(
            LunarDate(year, month, day, is_leap_month), provider=eng
        )
        return cls.from_solar(
            solar.year,
            solar.month,
            solar.day,
            hour,
            minute,
            second,
            timezone=timezone,
            rules=rules,
            provider=eng,
        )

    @classmethod
    def from_datetime(
        cls,
        instant: datetime,
        *,
        rules: Optional[GanzhiRules] = None,
        provider: Optional[CalendarProvider] = None,
    ) -> LunarCalendar:
        return cls(instant, rules=rules, provider=provider)

    @property
    def instant(self) -> datetime:
        return self._instant

    @property
    def timezone(self) -> str:
        key = getattr(self._instant.tzinfo, "key", None)
        if isinstance(key, str) and key:
            return key
        return str(self._instant.tzinfo)

    @property
    def solar(self) -> SolarDate:
        return self._solar

    @property
    def lunar(self) -> LunarDate:
        return self._lunar

    @property
    def zodiac(self) -> Zodiac:
        return self._zodiac

    @property
    def year_ganzhi(self) -> Ganzhi:
        return self._pillars.year

    @property
    def pillars(self) -> GanzhiPillars:
        return self._pillars

    @property
    def previous_solar_term(self) -> SolarTerm:
        return self._previous_solar_term

    @property
    def next_solar_term(self) -> SolarTerm:
        return self._next_solar_term

    @property
    def rules(self) -> GanzhiRules:
        return self._rules

    @property
    def provider_name(self) -> str:
        return getattr(self._provider, "name", type(self._provider).__name__)

    @overload
    def ganzhi(
        self,
        *,
        rules: Optional[GanzhiRules] = None,
        explain: Literal[False] = False,
    ) -> GanzhiPillars: ...

    @overload
    def ganzhi(
        self,
        *,
        rules: Optional[GanzhiRules] = None,
        explain: Literal[True],
    ) -> tuple[GanzhiPillars, GanzhiTrace]: ...

    def ganzhi(
        self,
        *,
        rules: Optional[GanzhiRules] = None,
        explain: bool = False,
    ) -> Union[GanzhiPillars, tuple[GanzhiPillars, GanzhiTrace]]:
        """
        Four pillars under explicit rules.

        explain=True returns (pillars, deterministic rule trace).
        """
        active = rules or self._rules
        if rules is None and not explain:
            return self._pillars
        pillars, _zodiac, trace = compute_pillars(
            self._instant,
            self._lunar,
            rules=active,
            provider=self._provider,
        )
        if explain:
            return pillars, trace
        return pillars

    def snapshot(self) -> CalendarSnapshot:
        return CalendarSnapshot(
            instant=self._instant,
            timezone=self.timezone,
            solar=self._solar,
            lunar=self._lunar,
            zodiac=self._zodiac,
            ganzhi=self._pillars,
            rules=self._rules,
            provider=self.provider_name,
            previous_solar_term=self._previous_solar_term,
            next_solar_term=self._next_solar_term,
        )

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot().to_dict()
