# -*- coding: utf-8 -*-
"""Four-pillar computation and rule traces."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from mystilink_lunar.ganzhi.day import compute_day_pillar
from mystilink_lunar.ganzhi.hour import compute_hour_pillar
from mystilink_lunar.ganzhi.month import compute_month_pillar
from mystilink_lunar.ganzhi.year import compute_year_pillar, ganzhi_from_year_number
from mystilink_lunar.models import (
    GanzhiPillars,
    GanzhiRules,
    GanzhiTrace,
    LunarDate,
    Zodiac,
)
from mystilink_lunar.providers import CalendarProvider, default_provider


def compute_pillars(
    instant: datetime,
    lunar: LunarDate,
    *,
    rules: GanzhiRules,
    provider: Optional[CalendarProvider] = None,
) -> tuple[GanzhiPillars, Zodiac, GanzhiTrace]:
    """Compute four pillars, zodiac, and a deterministic rule trace."""
    eng = provider or default_provider()
    year_gz, zodiac, year_trace = compute_year_pillar(
        lunar, rules=rules, instant=instant, provider=eng
    )
    month_gz, month_trace = compute_month_pillar(
        lunar,
        year_stem_index=year_gz.stem_index,
        rules=rules,
        instant=instant,
        provider=eng,
    )
    day_gz, day_trace, _day_date = compute_day_pillar(instant, rules=rules)
    hour_gz, hour_trace = compute_hour_pillar(
        instant, day_stem_index=day_gz.stem_index, rules=rules
    )
    pillars = GanzhiPillars(year=year_gz, month=month_gz, day=day_gz, hour=hour_gz)
    trace = GanzhiTrace(
        year=year_trace,
        month=month_trace,
        day=day_trace,
        hour=hour_trace,
        rules=rules,
    )
    return pillars, zodiac, trace


__all__ = [
    "compute_pillars",
    "ganzhi_from_year_number",
]
