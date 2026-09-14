# -*- coding: utf-8 -*-
"""Calendar provider protocol."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from mystilink_lunar.models import LunarDate, SolarDate


@runtime_checkable
class CalendarProvider(Protocol):
    """Internal provider boundary; public APIs must not expose provider types."""

    name: str

    def solar_to_lunar(self, solar: SolarDate) -> LunarDate:
        ...

    def lunar_to_solar(self, lunar: LunarDate) -> SolarDate:
        ...
