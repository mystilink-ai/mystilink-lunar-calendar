# -*- coding: utf-8 -*-
"""Ganzhi helpers for year pillar / zodiac (alpha.1)."""
from __future__ import annotations

from mystilink_lunar.constants import SEXAGENARY_EPOCH_YEAR
from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import Ganzhi, GanzhiRules, LunarDate, Zodiac


def ganzhi_from_year_number(year: int) -> Ganzhi:
    """Map a calendar year number to stem-branch via (year - 4) mod 60."""
    idx = (year - SEXAGENARY_EPOCH_YEAR) % 60
    return Ganzhi(stem_index=idx % 10, branch_index=idx % 12)


def zodiac_from_branch_index(branch_index: int) -> Zodiac:
    return Zodiac(branch_index=branch_index)


def year_ganzhi_and_zodiac(
    lunar: LunarDate,
    *,
    rules: GanzhiRules,
) -> tuple[Ganzhi, Zodiac]:
    """
    Resolve year pillar and zodiac for alpha.1.

    Supported:
      - chunjie: use lunar year number (春节换年)
    Unsupported yet (raise):
      - lichun_day / lichun_exact (arrive with solar terms in alpha.2+)
    """
    if rules.year_boundary == "chunjie":
        gz = ganzhi_from_year_number(lunar.year)
        return gz, zodiac_from_branch_index(gz.branch_index)
    raise MystilinkLunarError(
        f"year_boundary={rules.year_boundary!r} requires solar-term support "
        "(planned for alpha.2+); use GanzhiRules.lunar_calendar() for now"
    )
