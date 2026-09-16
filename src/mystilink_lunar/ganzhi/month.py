# -*- coding: utf-8 -*-
"""Month pillar."""
from __future__ import annotations

from datetime import datetime

from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import Ganzhi, GanzhiRules, LunarDate, PillarTrace
from mystilink_lunar.providers import CalendarProvider
from mystilink_lunar.solar_terms.definitions import solar_term_def
from mystilink_lunar.timezone import require_aware

# 节 index → month branch index (丑..子)
_JIE_TO_BRANCH = {
    1: 1,  # 小寒 → 丑
    3: 2,  # 立春 → 寅
    5: 3,  # 惊蛰 → 卯
    7: 4,  # 清明 → 辰
    9: 5,  # 立夏 → 巳
    11: 6,  # 芒种 → 午
    13: 7,  # 小暑 → 未
    15: 8,  # 立秋 → 申
    17: 9,  # 白露 → 酉
    19: 10,  # 寒露 → 戌
    21: 11,  # 立冬 → 亥
    23: 0,  # 大雪 → 子
}

# 五虎遁: year stem → 寅月 stem index
_YIN_MONTH_STEM = (2, 4, 6, 8, 0, 2, 4, 6, 8, 0)  # 甲→丙 … 癸→甲


def month_stem_from_year(year_stem_index: int, month_branch_index: int) -> int:
    """五虎遁: stem for a month branch given year stem."""
    yin_stem = _YIN_MONTH_STEM[year_stem_index]
    # 寅=2 is order 0
    order = (month_branch_index - 2) % 12
    return (yin_stem + order) % 10


def _previous_jie(
    instant: datetime,
    *,
    provider: CalendarProvider,
    exact: bool,
) -> tuple[int, datetime]:
    """Return (jie_index, jie_datetime_in_instant_tz)."""
    aware = require_aware(instant)
    tz = aware.tzinfo
    assert tz is not None

    events: list[tuple[int, datetime]] = []
    for year in (aware.year - 1, aware.year, aware.year + 1):
        for index, shanghai in provider.solar_term_events(year):
            if index in _JIE_TO_BRANCH:
                events.append((index, shanghai.astimezone(tz)))

    uniq: dict[str, tuple[int, datetime]] = {}
    for index, dt in events:
        uniq[f"{index}:{dt.isoformat()}"] = (index, dt)
    ordered = sorted(uniq.values(), key=lambda item: item[1])

    previous: tuple[int, datetime] | None = None
    for index, dt in ordered:
        if exact:
            if dt <= aware:
                previous = (index, dt)
        else:
            if dt.date() <= aware.date():
                previous = (index, dt)
    if previous is None:
        raise MystilinkLunarError("failed to resolve previous jie for month pillar")
    return previous


def compute_month_pillar(
    lunar: LunarDate,
    *,
    year_stem_index: int,
    rules: GanzhiRules,
    instant: datetime,
    provider: CalendarProvider,
) -> tuple[Ganzhi, PillarTrace]:
    if rules.month_boundary == "lunar_month":
        branch_index = (lunar.month + 1) % 12  # 正月→寅
        stem_index = month_stem_from_year(year_stem_index, branch_index)
        gz = Ganzhi(stem_index=stem_index, branch_index=branch_index)
        leap = "leap " if lunar.is_leap_month else ""
        reason = (
            f"Lunar {leap}month {lunar.month} maps to branch index {branch_index} "
            f"(lunar_month); stem via 五虎遁 from year stem index {year_stem_index}."
        )
        return gz, PillarTrace(
            value=gz.text,
            stem_index=stem_index,
            branch_index=branch_index,
            boundary=rules.month_boundary,
            reason=reason,
        )

    if rules.month_boundary in ("jie_exact", "jie_day"):
        exact = rules.month_boundary == "jie_exact"
        jie_index, jie_dt = _previous_jie(instant, provider=provider, exact=exact)
        branch_index = _JIE_TO_BRANCH[jie_index]
        stem_index = month_stem_from_year(year_stem_index, branch_index)
        gz = Ganzhi(stem_index=stem_index, branch_index=branch_index)
        term = solar_term_def(jie_index)
        cmp = "instant" if exact else "civil date"
        reason = (
            f"Previous jie is {term.chinese_name} at {jie_dt.isoformat()} "
            f"({rules.month_boundary}, compared by {cmp}); month branch "
            f"{gz.branch}, stem via 五虎遁."
        )
        return gz, PillarTrace(
            value=gz.text,
            stem_index=stem_index,
            branch_index=branch_index,
            boundary=rules.month_boundary,
            reason=reason,
        )

    raise MystilinkLunarError(f"unsupported month_boundary: {rules.month_boundary!r}")
