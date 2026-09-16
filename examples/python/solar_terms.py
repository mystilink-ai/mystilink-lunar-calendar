# -*- coding: utf-8 -*-
"""Lookup a solar term instant."""
from mystilink_lunar import get_solar_term

term = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
print(term.chinese_name, term.datetime.isoformat(), f"λ={term.solar_longitude:g}")
