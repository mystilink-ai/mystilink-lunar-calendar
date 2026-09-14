# -*- coding: utf-8 -*-
"""Lunar conversion helpers."""
from __future__ import annotations

from mystilink_lunar.models import LunarDate, SolarDate
from mystilink_lunar.providers import CalendarProvider, default_provider


def solar_to_lunar(
    solar: SolarDate,
    *,
    provider: CalendarProvider | None = None,
) -> LunarDate:
    eng = provider or default_provider()
    return eng.solar_to_lunar(solar)


def lunar_to_solar(
    lunar: LunarDate,
    *,
    provider: CalendarProvider | None = None,
) -> SolarDate:
    eng = provider or default_provider()
    return eng.lunar_to_solar(lunar)
