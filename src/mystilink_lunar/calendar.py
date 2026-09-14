# -*- coding: utf-8 -*-
"""LunarCalendar facade."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from mystilink_lunar.ganzhi import year_ganzhi_and_zodiac
from mystilink_lunar.lunar import lunar_to_solar, solar_to_lunar
from mystilink_lunar.models import (
    CalendarSnapshot,
    Ganzhi,
    GanzhiRules,
    LunarDate,
    SolarDate,
    Zodiac,
)
from mystilink_lunar.providers import CalendarProvider, default_provider
from mystilink_lunar.timezone import build_aware_datetime, civil_date_in_zone, require_aware


class LunarCalendar:
    """
    Timezone-aware Chinese lunar calendar snapshot.

    Alpha.1: solar↔lunar, leap month, year ganzhi/zodiac (chunjie boundary), JSON.
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
        self._year_ganzhi, self._zodiac = year_ganzhi_and_zodiac(
            self._lunar, rules=self._rules
        )

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
        return self._year_ganzhi

    @property
    def rules(self) -> GanzhiRules:
        return self._rules

    @property
    def provider_name(self) -> str:
        return getattr(self._provider, "name", type(self._provider).__name__)

    def snapshot(self) -> CalendarSnapshot:
        return CalendarSnapshot(
            instant=self._instant,
            timezone=self.timezone,
            solar=self._solar,
            lunar=self._lunar,
            zodiac=self._zodiac,
            year_ganzhi=self._year_ganzhi,
            rules=self._rules,
            provider=self.provider_name,
        )

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot().to_dict()
