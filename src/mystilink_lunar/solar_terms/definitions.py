# -*- coding: utf-8 -*-
"""24 solar terms definitions (index-first; 冬至 = 0)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Final, Tuple


@dataclass(frozen=True)
class SolarTermDef:
    index: int
    id: str
    name: str
    chinese_name: str
    solar_longitude: float


# sxtwl jqIndex convention: 0 = 冬至 … 23 = 大雪
SOLAR_TERM_DEFS: Final[Tuple[SolarTermDef, ...]] = (
    SolarTermDef(0, "dongzhi", "Dong Zhi", "冬至", 270.0),
    SolarTermDef(1, "xiaohan", "Xiao Han", "小寒", 285.0),
    SolarTermDef(2, "dahan", "Da Han", "大寒", 300.0),
    SolarTermDef(3, "lichun", "Li Chun", "立春", 315.0),
    SolarTermDef(4, "yushui", "Yu Shui", "雨水", 330.0),
    SolarTermDef(5, "jingzhe", "Jing Zhe", "惊蛰", 345.0),
    SolarTermDef(6, "chunfen", "Chun Fen", "春分", 0.0),
    SolarTermDef(7, "qingming", "Qing Ming", "清明", 15.0),
    SolarTermDef(8, "guyu", "Gu Yu", "谷雨", 30.0),
    SolarTermDef(9, "lixia", "Li Xia", "立夏", 45.0),
    SolarTermDef(10, "xiaoman", "Xiao Man", "小满", 60.0),
    SolarTermDef(11, "mangzhong", "Mang Zhong", "芒种", 75.0),
    SolarTermDef(12, "xiazhi", "Xia Zhi", "夏至", 90.0),
    SolarTermDef(13, "xiaoshu", "Xiao Shu", "小暑", 105.0),
    SolarTermDef(14, "dashu", "Da Shu", "大暑", 120.0),
    SolarTermDef(15, "liqiu", "Li Qiu", "立秋", 135.0),
    SolarTermDef(16, "chushu", "Chu Shu", "处暑", 150.0),
    SolarTermDef(17, "bailu", "Bai Lu", "白露", 165.0),
    SolarTermDef(18, "qiufen", "Qiu Fen", "秋分", 180.0),
    SolarTermDef(19, "hanlu", "Han Lu", "寒露", 195.0),
    SolarTermDef(20, "shuangjiang", "Shuang Jiang", "霜降", 210.0),
    SolarTermDef(21, "lidong", "Li Dong", "立冬", 225.0),
    SolarTermDef(22, "xiaoxue", "Xiao Xue", "小雪", 240.0),
    SolarTermDef(23, "daxue", "Da Xue", "大雪", 255.0),
)

# Mid-qi (中气): every even index in the 冬至-first ordering
ZHONGQI_INDICES: Final[frozenset[int]] = frozenset(range(0, 24, 2))

_BY_INDEX: Final[Dict[int, SolarTermDef]] = {d.index: d for d in SOLAR_TERM_DEFS}
_BY_ID: Final[Dict[str, SolarTermDef]] = {d.id: d for d in SOLAR_TERM_DEFS}
_BY_CHINESE: Final[Dict[str, SolarTermDef]] = {
    d.chinese_name: d for d in SOLAR_TERM_DEFS
}


def solar_term_def(index: int) -> SolarTermDef:
    try:
        return _BY_INDEX[index]
    except KeyError as exc:
        raise KeyError(f"solar term index out of range: {index}") from exc


def resolve_solar_term_key(key: str | int) -> SolarTermDef:
    """Accept index, id (`lichun`), UPPER id, or Chinese name (`立春`)."""
    if isinstance(key, int):
        return solar_term_def(key)
    text = key.strip()
    if not text:
        raise KeyError("empty solar term key")
    if text.isdigit():
        return solar_term_def(int(text))
    lower = text.lower().replace(" ", "").replace("_", "")
    # normalize "Li Chun" / "LI_CHUN" / "lichun"
    compact_ids = {d.id.replace("_", ""): d for d in SOLAR_TERM_DEFS}
    if lower in compact_ids:
        return compact_ids[lower]
    if text in _BY_CHINESE:
        return _BY_CHINESE[text]
    raise KeyError(f"unknown solar term: {key!r}")
