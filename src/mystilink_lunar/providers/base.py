# -*- coding: utf-8 -*-
"""Calendar provider protocol."""
from __future__ import annotations

from datetime import datetime
from typing import List, Protocol, Tuple, runtime_checkable

from mystilink_lunar.models import LunarDate, SolarDate


@runtime_checkable
class CalendarProvider(Protocol):
    """Internal provider boundary; public APIs must not expose provider types."""

    name: str

    def solar_to_lunar(self, solar: SolarDate) -> LunarDate:
        ...

    def lunar_to_solar(self, lunar: LunarDate) -> SolarDate:
        ...

    def solar_term_events(self, year: int) -> List[Tuple[int, datetime]]:
        """(jq_index, Asia/Shanghai-aware datetime) for getJieQiByYear(year)."""
        ...

    def solar_term_instant(
        self, index: int, year: int, *, timezone: str
    ) -> datetime:
        ...
