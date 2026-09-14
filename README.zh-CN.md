# Mystilink 农历历法库

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## 概述

面向术数引擎与 Agent 工具的确定性、时区感知中国农历与干支基础库。提供公历 ↔ 农历（含闰月）转换与结构化 JSON，并将历法事实与八字 / 紫微等上层规则引擎分离。

**v0.1.0a1（历法基础）** 包含：公农互转、闰月、强制 IANA 时区、年柱干支与生肖（`chunjie` 边界）、`to_dict()`、CLI `convert`。二十四节气与完整四柱在后续 alpha 提供。

## 平台与语言

| 目标 | 交付（alpha.1） |
|------|-----------------|
| Python 3.10+ | 可安装包 `mystilink-lunar`，CLI `mystilink-lunar` |
| C / C++ / C# / Java / JavaScript·Node | 计划：基于 CLI JSON 的薄绑定（与同系计算器一致） |

## 环境要求

- Python 3.10 或更高
- 运行时 provider：`sxtwl`（已写入依赖；不出现在公开 import 面）

## 安装与快速开始

```bash
cd mystilink-lunar-calendar
python3 -m pip install -e ".[dev]"

mystilink-lunar convert \
  --date 1993-09-28 \
  --time 13:21 \
  --timezone Asia/Shanghai

mystilink-lunar convert \
  --date 1993-09-28 \
  --time 13:21 \
  --timezone Asia/Shanghai \
  --json
```

也可：

```bash
python3 -m mystilink_lunar convert --date 1993-09-28 --timezone Asia/Shanghai --json
```

## Python API

```python
from mystilink_lunar import LunarCalendar, GanzhiRules

cal = LunarCalendar.from_solar(
    year=1993,
    month=9,
    day=28,
    hour=13,
    minute=21,
    timezone="Asia/Shanghai",
    rules=GanzhiRules.lunar_calendar(),
)

cal.solar          # SolarDate
cal.lunar          # LunarDate(year=1993, month=8, day=13, is_leap_month=False)
cal.year_ganzhi    # Ganzhi → 癸酉
cal.zodiac         # Zodiac id "rooster"
cal.to_dict()      # 结构化字典 / 可直接 JSON
```

时区**必填**。naive datetime 会抛出 `MissingTimezoneError`。

农历 → 公历：

```python
cal = LunarCalendar.from_lunar(
    2023, 2, 1,
    is_leap_month=True,
    timezone="Asia/Shanghai",
)
```

## CLI

| 命令 | 说明 |
|------|------|
| `convert` | 公历或农历输入 → 历法快照 |
| `version` | 包版本 |

### convert

| 选项 | 说明 |
|------|------|
| `--date` | 公历 `YYYY-MM-DD` |
| `--lunar` | 农历 `YYYY-MM-DD` |
| `--leap` | 将 `--lunar` 视为闰月 |
| `--time` | `HH:MM` 或 `HH:MM:SS`（默认 `00:00:00`） |
| `--timezone` | IANA 时区（**必填**） |
| `--year-boundary` | `chunjie`（默认；alpha.1 仅实现此边界） |
| `--json` | 输出符合 `schema/convert.output.json` 的 JSON |

## 配置 / 规则

- `GanzhiRules.year_boundary`：`chunjie` | `lichun_day` | `lichun_exact`
- alpha.1 仅实现 `chunjie`；其余取值在节气落地前会报错
- 细节见 [docs/calendar-rules.md](docs/calendar-rules.md)

## 示例

- [examples/python/basic.py](examples/python/basic.py)

## 精度

见 [docs/accuracy.md](docs/accuracy.md)。本 alpha 支持的公历年份：**1900–2100**。

## 路线图（摘要）

| 版本 | 重点 |
|------|------|
| 0.1.0a1 | 历法基础（本版本） |
| alpha.2 | 二十四节气精确到秒 |
| alpha.3 | 干支四柱 + 规则追溯 |
| 0.2+ | 自建天文核心；去掉运行时 sxtwl |
| 1.0 | 稳定 schema、权威 fixture、零运行时依赖 |

## 限制

- 尚未计算月/日/时柱与节气对象
- 除 `chunjie` 外的年界不可用
- 公开 API 不得 import 或暴露 `sxtwl`
- alpha.1 未交付 Python 以外的语言矩阵绑定

## 许可

MIT。见 [LICENSE](LICENSE)。第三方运行时说明：[NOTICE](NOTICE)。

## 问题反馈

请附带：CLI 版本（`mystilink-lunar version`）、完整命令行（仅使用虚构日期）、stdout/stderr。
