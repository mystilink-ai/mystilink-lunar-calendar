# -*- coding: utf-8 -*-
"""Hour pillar (时辰)."""
from __future__ import annotations

from datetime import datetime

from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import Ganzhi, GanzhiRules, PillarTrace
from mystilink_lunar.timezone import require_aware

# 五鼠遁: day stem → 子时 stem index
_ZI_HOUR_STEM = (0, 2, 4, 6, 8, 0, 2, 4, 6, 8)  # 甲→甲 … 癸→壬


def shichen_index(hour: int, minute: int = 0) -> int:
    """Map local clock time to 时辰 index (0=子 … 11=亥)."""
    total = hour * 60 + minute
    return ((total + 60) % 1440) // 120


def hour_stem_from_day(day_stem_index: int, shichen: int) -> int:
    """五鼠遁."""
    return (_ZI_HOUR_STEM[day_stem_index] + shichen) % 10


def compute_hour_pillar(
    instant: datetime,
    *,
    day_stem_index: int,
    rules: GanzhiRules,
) -> tuple[Ganzhi, PillarTrace]:
    if rules.hour_system != "double_hour":
        raise MystilinkLunarError(f"unsupported hour_system: {rules.hour_system!r}")

    aware = require_aware(instant)
    shi = shichen_index(aware.hour, aware.minute)
    stem_index = hour_stem_from_day(day_stem_index, shi)
    gz = Ganzhi(stem_index=stem_index, branch_index=shi)
    reason = (
        f"Clock {aware.strftime('%H:%M')} maps to shichen index {shi} "
        f"(double_hour); stem via 五鼠遁 from day stem index {day_stem_index}."
    )
    return gz, PillarTrace(
        value=gz.text,
        stem_index=stem_index,
        branch_index=shi,
        boundary=rules.hour_system,
        reason=reason,
    )
