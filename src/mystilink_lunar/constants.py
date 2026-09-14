# -*- coding: utf-8 -*-
"""Stem, branch, and zodiac constants (index-first)."""
from __future__ import annotations

from typing import Final, Tuple

# Heavenly stems 天干: 甲=0 … 癸=9
STEMS: Final[Tuple[str, ...]] = (
    "甲",
    "乙",
    "丙",
    "丁",
    "戊",
    "己",
    "庚",
    "辛",
    "壬",
    "癸",
)

# Earthly branches 地支: 子=0 … 亥=11
BRANCHES: Final[Tuple[str, ...]] = (
    "子",
    "丑",
    "寅",
    "卯",
    "辰",
    "巳",
    "午",
    "未",
    "申",
    "酉",
    "戌",
    "亥",
)

# Zodiac keyed by branch index; English id is stable for JSON
ZODIAC_EN: Final[Tuple[str, ...]] = (
    "rat",
    "ox",
    "tiger",
    "rabbit",
    "dragon",
    "snake",
    "horse",
    "goat",
    "monkey",
    "rooster",
    "dog",
    "pig",
)

ZODIAC_ZH: Final[Tuple[str, ...]] = (
    "鼠",
    "牛",
    "虎",
    "兔",
    "龙",
    "蛇",
    "马",
    "羊",
    "猴",
    "鸡",
    "狗",
    "猪",
)

# Sexagenary: year 甲子 ≈ Gregorian/Lunar year 1984 when using (year - 4) % 60
SEXAGENARY_EPOCH_YEAR: Final[int] = 4
