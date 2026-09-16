# -*- coding: utf-8 -*-
"""Day pillar."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import Ganzhi, GanzhiRules, PillarTrace
from mystilink_lunar.timezone import require_aware

# Verified against sxtwl for 1900–2100 samples: 1900-01-31 = 甲辰
_DAY_EPOCH = date(1900, 1, 31)


def ganzhi_from_civil_date(d: date) -> Ganzhi:
    days = (d - _DAY_EPOCH).days
    return Ganzhi(stem_index=days % 10, branch_index=(days + 4) % 12)


def resolve_day_date(instant: datetime, *, rules: GanzhiRules) -> tuple[date, str]:
    aware = require_aware(instant)
    civil = aware.date()
    if rules.day_boundary == "midnight":
        return civil, f"Civil date {civil.isoformat()} (midnight boundary)."
    if rules.day_boundary == "zi_start":
        if aware.hour >= 23:
            nxt = civil + timedelta(days=1)
            return (
                nxt,
                f"Local time {aware.strftime('%H:%M:%S')} is in late 子时; "
                f"day pillar uses next civil date {nxt.isoformat()} (zi_start).",
            )
        return (
            civil,
            f"Local time {aware.strftime('%H:%M:%S')} uses civil date "
            f"{civil.isoformat()} (zi_start).",
        )
    raise MystilinkLunarError(f"unsupported day_boundary: {rules.day_boundary!r}")


def compute_day_pillar(
    instant: datetime,
    *,
    rules: GanzhiRules,
) -> tuple[Ganzhi, PillarTrace, date]:
    day_date, reason = resolve_day_date(instant, rules=rules)
    gz = ganzhi_from_civil_date(day_date)
    trace = PillarTrace(
        value=gz.text,
        stem_index=gz.stem_index,
        branch_index=gz.branch_index,
        boundary=rules.day_boundary,
        reason=reason,
    )
    return gz, trace, day_date
