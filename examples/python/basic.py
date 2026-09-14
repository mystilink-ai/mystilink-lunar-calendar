# -*- coding: utf-8 -*-
"""Minimal solar → lunar example."""
from mystilink_lunar import LunarCalendar

cal = LunarCalendar.from_solar(
    year=1993,
    month=9,
    day=28,
    hour=13,
    minute=21,
    timezone="Asia/Shanghai",
)

print(cal.lunar)
print(cal.year_ganzhi.text, cal.zodiac.id)
print(cal.to_dict())
