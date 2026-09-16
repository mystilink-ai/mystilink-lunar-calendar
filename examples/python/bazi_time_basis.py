# -*- coding: utf-8 -*-
"""BaZi-oriented time basis using explicit GanzhiRules."""
from mystilink_lunar import GanzhiRules, LunarCalendar

cal = LunarCalendar.from_solar(
    1993, 9, 28, 13, 21,
    timezone="Asia/Shanghai",
    rules=GanzhiRules.bazi_default(),
)

pillars, trace = cal.ganzhi(explain=True)
print(pillars.year.text, pillars.month.text, pillars.day.text, pillars.hour.text)
print(trace.year.reason)
print(trace.month.reason)
