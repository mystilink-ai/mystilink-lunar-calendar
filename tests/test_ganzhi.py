# -*- coding: utf-8 -*-
"""Four-pillar and explain tests."""
from __future__ import annotations

from datetime import timedelta

from mystilink_lunar import GanzhiRules, LunarCalendar, get_solar_term


def test_four_pillars_1993_09_28() -> None:
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai",
        rules=GanzhiRules.bazi_default(),
    )
    p = cal.pillars
    assert p.year.text == "癸酉"
    assert p.month.text == "辛酉"
    assert p.day.text == "壬子"
    assert p.hour.text == "丁未"


def test_explain_trace() -> None:
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai",
        rules=GanzhiRules.bazi_default(),
    )
    pillars, trace = cal.ganzhi(explain=True)
    assert pillars.day.text == "壬子"
    assert trace.year.boundary == "lichun_exact"
    assert trace.month.boundary == "jie_exact"
    assert "白露" in trace.month.reason or "jie_exact" in trace.month.reason
    assert trace.day.boundary == "zi_start"
    assert trace.hour.boundary == "double_hour"
    data = trace.to_dict()
    assert data["year"]["value"] == "癸酉"


def test_liqiu_month_boundary_exact() -> None:
    liqiu = get_solar_term("liqiu", 1993, timezone="Asia/Shanghai").datetime
    rules = GanzhiRules.bazi_default()
    before = LunarCalendar.from_datetime(liqiu - timedelta(seconds=1), rules=rules)
    after = LunarCalendar.from_datetime(liqiu + timedelta(seconds=1), rules=rules)
    assert before.pillars.month.text == "己未"
    assert after.pillars.month.text == "庚申"
    assert before.next_solar_term.id == "liqiu"
    assert after.previous_solar_term.id == "liqiu"


def test_zi_start_day_and_hour() -> None:
    rules = GanzhiRules.bazi_default()
    at_2259 = LunarCalendar.from_solar(
        1993, 9, 28, 22, 59, timezone="Asia/Shanghai", rules=rules
    )
    at_2300 = LunarCalendar.from_solar(
        1993, 9, 28, 23, 0, timezone="Asia/Shanghai", rules=rules
    )
    at_0000 = LunarCalendar.from_solar(
        1993, 9, 29, 0, 0, timezone="Asia/Shanghai", rules=rules
    )
    at_0100 = LunarCalendar.from_solar(
        1993, 9, 29, 1, 0, timezone="Asia/Shanghai", rules=rules
    )

    assert at_2259.pillars.day.text == "壬子"
    assert at_2259.pillars.hour.text == "辛亥"  # 戌时 ends 22:59 → wait 22:59 is 亥?
    # 21:00-22:59 = 亥, 23:00-00:59 = 子
    assert at_2259.pillars.hour.branch == "亥"

    assert at_2300.pillars.day.text == "癸丑"  # rolls to next day
    assert at_2300.pillars.hour.text == "壬子"  # 子时 with next day stem

    assert at_0000.pillars.day.text == "癸丑"
    assert at_0000.pillars.hour.text == "壬子"

    assert at_0100.pillars.day.text == "癸丑"
    assert at_0100.pillars.hour.branch == "丑"


def test_midnight_keeps_day_at_2300() -> None:
    rules = GanzhiRules(
        year_boundary="lichun_exact",
        month_boundary="jie_exact",
        day_boundary="midnight",
        hour_system="double_hour",
    )
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 23, 0, timezone="Asia/Shanghai", rules=rules
    )
    assert cal.pillars.day.text == "壬子"
    assert cal.pillars.hour.text == "庚子"  # 子时 with same-day stem 壬 → 庚子


def test_lunar_month_profile_month_branch() -> None:
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai",
        rules=GanzhiRules.lunar_calendar(),
    )
    # lunar month 8 → 酉
    assert cal.pillars.month.branch == "酉"
    assert cal.pillars.month.text == "辛酉"
