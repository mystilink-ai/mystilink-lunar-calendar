# -*- coding: utf-8 -*-
"""24 solar terms tests."""
from __future__ import annotations

from datetime import timedelta

import pytest

from mystilink_lunar import (
    GanzhiRules,
    LunarCalendar,
    UnknownSolarTermError,
    get_solar_term,
)


def test_lichun_2026_shanghai_to_the_second() -> None:
    term = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
    assert term.index == 3
    assert term.id == "lichun"
    assert term.chinese_name == "立春"
    assert term.solar_longitude == 315.0
    assert term.datetime.year == 2026
    assert term.datetime.month == 2
    assert term.datetime.day == 4
    assert term.datetime.hour == 4
    assert term.datetime.minute == 1
    assert term.datetime.tzinfo is not None
    assert getattr(term.datetime.tzinfo, "key", None) == "Asia/Shanghai"


def test_get_solar_term_aliases() -> None:
    a = get_solar_term("LICHUN", 2026, timezone="Asia/Shanghai")
    b = get_solar_term("立春", 2026, timezone="Asia/Shanghai")
    c = get_solar_term(3, 2026, timezone="Asia/Shanghai")
    assert a.datetime == b.datetime == c.datetime


def test_unknown_solar_term() -> None:
    with pytest.raises(UnknownSolarTermError):
        get_solar_term("not-a-term", 2026, timezone="Asia/Shanghai")


def test_lichun_timezone_conversion() -> None:
    sh = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
    utc = get_solar_term("lichun", 2026, timezone="UTC")
    assert sh.datetime.utcoffset() != utc.datetime.utcoffset()
    assert sh.datetime.astimezone(utc.datetime.tzinfo) == utc.datetime


def test_lichun_exact_plus_minus_one_second() -> None:
    lichun = get_solar_term("lichun", 2026, timezone="Asia/Shanghai").datetime
    rules = GanzhiRules.bazi_default()
    before = LunarCalendar.from_datetime(lichun - timedelta(seconds=1), rules=rules)
    at = LunarCalendar.from_datetime(lichun, rules=rules)
    after = LunarCalendar.from_datetime(lichun + timedelta(seconds=1), rules=rules)

    assert before.year_ganzhi.text == "乙巳"  # 2025
    assert at.year_ganzhi.text == "丙午"  # 2026
    assert after.year_ganzhi.text == "丙午"

    assert before.next_solar_term.id == "lichun"
    assert at.previous_solar_term.id == "lichun"
    assert after.previous_solar_term.id == "lichun"


def test_lichun_day_vs_exact() -> None:
    """Same civil day, before the exact instant: day rule already crossed, exact has not."""
    lichun = get_solar_term("lichun", 2026, timezone="Asia/Shanghai").datetime
    early = lichun.replace(hour=0, minute=0, second=0, microsecond=0)
    assert early < lichun

    by_day = LunarCalendar.from_datetime(early, rules=GanzhiRules(year_boundary="lichun_day"))
    by_exact = LunarCalendar.from_datetime(early, rules=GanzhiRules(year_boundary="lichun_exact"))
    assert by_day.year_ganzhi.text == "丙午"
    assert by_exact.year_ganzhi.text == "乙巳"


def test_jingzhe_plus_minus_one_second() -> None:
    jingzhe = get_solar_term("jingzhe", 2026, timezone="Asia/Shanghai").datetime
    before = LunarCalendar.from_datetime(jingzhe - timedelta(seconds=1))
    after = LunarCalendar.from_datetime(jingzhe + timedelta(seconds=1))
    assert before.next_solar_term.id == "jingzhe"
    assert after.previous_solar_term.id == "jingzhe"


def test_convert_snapshot_includes_adjacent_terms() -> None:
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai"
    )
    assert cal.previous_solar_term.id == "qiufen"
    assert cal.next_solar_term.id == "hanlu"
    data = cal.to_dict()
    assert data["solar_term"]["previous"]["chinese_name"] == "秋分"
    assert data["solar_term"]["next"]["chinese_name"] == "寒露"
