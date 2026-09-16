# -*- coding: utf-8 -*-
"""Solar ↔ lunar conversion tests."""
from __future__ import annotations

import pytest

from mystilink_lunar import LunarCalendar, LunarDate, MissingTimezoneError, SolarDate
from mystilink_lunar.lunar import lunar_to_solar, solar_to_lunar
from mystilink_lunar.timezone import build_aware_datetime


def test_1993_09_28_to_lunar() -> None:
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai"
    )
    assert cal.lunar == LunarDate(1993, 8, 13, False)
    assert cal.year_ganzhi.text == "癸酉"
    assert cal.zodiac.id == "rooster"
    assert cal.timezone == "Asia/Shanghai"


def test_lunar_to_solar_roundtrip() -> None:
    solar = lunar_to_solar(LunarDate(1993, 8, 13, False))
    assert solar == SolarDate(1993, 9, 28)
    back = solar_to_lunar(solar)
    assert back == LunarDate(1993, 8, 13, False)


def test_spring_festival_boundary_1993() -> None:
    before = LunarCalendar.from_solar(1993, 1, 22, timezone="Asia/Shanghai")
    after = LunarCalendar.from_solar(1993, 1, 23, timezone="Asia/Shanghai")
    assert before.lunar == LunarDate(1992, 12, 30, False)
    assert after.lunar == LunarDate(1993, 1, 1, False)
    assert before.zodiac.id == "monkey"  # 壬申
    assert after.zodiac.id == "rooster"  # 癸酉
    assert before.year_ganzhi.text == "壬申"
    assert after.year_ganzhi.text == "癸酉"


def test_leap_month_2023() -> None:
    cal = LunarCalendar.from_solar(2023, 3, 22, timezone="Asia/Shanghai")
    assert cal.lunar == LunarDate(2023, 2, 1, True)
    back = LunarCalendar.from_lunar(
        2023, 2, 1, is_leap_month=True, timezone="Asia/Shanghai"
    )
    assert back.solar == SolarDate(2023, 3, 22)


def test_missing_timezone_raises() -> None:
    with pytest.raises(MissingTimezoneError):
        build_aware_datetime(1993, 9, 28, timezone="")
    from datetime import datetime

    with pytest.raises(MissingTimezoneError):
        LunarCalendar.from_datetime(datetime(1993, 9, 28, 13, 21))


def test_to_dict_shape() -> None:
    data = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Asia/Shanghai"
    ).to_dict()
    assert data["solar"]["timezone"] == "Asia/Shanghai"
    assert data["solar"]["datetime"].startswith("1993-09-28T13:21:00")
    assert data["lunar"] == {
        "year": 1993,
        "month": 8,
        "day": 13,
        "is_leap_month": False,
    }
    assert data["ganzhi"]["year"]["text"] == "癸酉"
    assert data["ganzhi"]["month"]["text"] == "辛酉"
    assert data["ganzhi"]["day"]["text"] == "壬子"
    assert data["ganzhi"]["hour"]["text"] == "丁未"
    assert data["zodiac"]["id"] == "rooster"
    assert data["rules"]["year_boundary"] == "chunjie"
    assert data["rules"]["month_boundary"] == "lunar_month"
    assert data["rules"]["day_boundary"] == "midnight"
    assert data["solar_term"]["previous"]["id"] == "qiufen"
    assert data["solar_term"]["next"]["id"] == "hanlu"
    assert data["provider"] == "sxtwl"


def test_europe_london_civil_date() -> None:
    """Same wall-clock components in another zone stay civil-local for conversion."""
    cal = LunarCalendar.from_solar(
        1993, 9, 28, 13, 21, timezone="Europe/London"
    )
    assert cal.lunar == LunarDate(1993, 8, 13, False)
    assert cal.timezone == "Europe/London"
