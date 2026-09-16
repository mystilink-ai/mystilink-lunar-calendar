# -*- coding: utf-8 -*-
"""Year pillar."""
from __future__ import annotations

from datetime import datetime

from mystilink_lunar.constants import SEXAGENARY_EPOCH_YEAR
from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import Ganzhi, GanzhiRules, LunarDate, PillarTrace, Zodiac
from mystilink_lunar.providers import CalendarProvider
from mystilink_lunar.solar_terms import get_solar_term
from mystilink_lunar.timezone import require_aware


def ganzhi_from_year_number(year: int) -> Ganzhi:
    """Map a year number to stem-branch via (year - 4) mod 60."""
    idx = (year - SEXAGENARY_EPOCH_YEAR) % 60
    return Ganzhi(stem_index=idx % 10, branch_index=idx % 12)


def zodiac_from_branch_index(branch_index: int) -> Zodiac:
    return Zodiac(branch_index=branch_index)


def _timezone_key(instant: datetime) -> str:
    key = getattr(instant.tzinfo, "key", None)
    if isinstance(key, str) and key:
        return key
    raise MystilinkLunarError(
        "year boundary requires a ZoneInfo timezone with an IANA key"
    )


def resolve_ganzhi_year_number(
    lunar: LunarDate,
    *,
    rules: GanzhiRules,
    instant: datetime,
    provider: CalendarProvider,
) -> tuple[int, str]:
    """Return (year_num, reason)."""
    if rules.year_boundary == "chunjie":
        return lunar.year, f"Lunar year {lunar.year} (chunjie / 正月初一 boundary)."

    aware = require_aware(instant)
    tz = _timezone_key(aware)
    y = aware.year
    lichun = get_solar_term(3, y, timezone=tz, provider=provider).datetime
    if rules.year_boundary == "lichun_exact":
        crossed = aware >= lichun
        year_num = y if crossed else y - 1
        side = "on/after" if crossed else "before"
        return (
            year_num,
            f"Timestamp is {side} Li Chun {lichun.isoformat()} (lichun_exact).",
        )
    if rules.year_boundary == "lichun_day":
        crossed = aware.date() >= lichun.date()
        year_num = y if crossed else y - 1
        side = "on/after" if crossed else "before"
        return (
            year_num,
            f"Civil date {aware.date().isoformat()} is {side} Li Chun date "
            f"{lichun.date().isoformat()} (lichun_day).",
        )
    raise MystilinkLunarError(f"unsupported year_boundary: {rules.year_boundary!r}")


def compute_year_pillar(
    lunar: LunarDate,
    *,
    rules: GanzhiRules,
    instant: datetime,
    provider: CalendarProvider,
) -> tuple[Ganzhi, Zodiac, PillarTrace]:
    year_num, reason = resolve_ganzhi_year_number(
        lunar, rules=rules, instant=instant, provider=provider
    )
    gz = ganzhi_from_year_number(year_num)
    zodiac = zodiac_from_branch_index(gz.branch_index)
    trace = PillarTrace(
        value=gz.text,
        stem_index=gz.stem_index,
        branch_index=gz.branch_index,
        boundary=rules.year_boundary,
        reason=reason,
    )
    return gz, zodiac, trace
