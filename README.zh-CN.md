# Mystilink 农历历法库

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## 概述

面向术数引擎与 Agent 工具的确定性、时区感知中国农历与干支基础库。提供公历 ↔ 农历（含闰月）、二十四节气精确到秒、在显式规则下计算四柱，并输出结构化 JSON。

**v0.1.0a3（四柱）** 在 alpha.2 节气能力之上，增加月/日/时柱、`GanzhiRules` 配置档，以及 `ganzhi(explain=True)` 规则追溯。

## 平台与语言

| 目标 | 交付（alpha.3） |
|------|-----------------|
| Python 3.10+ | 可安装包 `mystilink-lunar`，CLI `lunar`（别名 `mystilink-lunar`） |
| C / C++ / C# / Java / JavaScript·Node | 计划：基于 CLI JSON 的薄绑定 |

## 环境要求

- Python 3.10 或更高
- 运行时 provider：`sxtwl`（已写入依赖；不出现在公开 import 面）

## 安装与快速开始

```bash
cd mystilink-lunar-calendar
python3 -m pip install -e ".[dev]"

lunar convert \
  --date 1993-09-28 \
  --time 13:21 \
  --timezone Asia/Shanghai \
  --profile bazi \
  --json
```

## Python API

```python
from mystilink_lunar import LunarCalendar, GanzhiRules, get_solar_term

cal = LunarCalendar.from_solar(
    1993, 9, 28, 13, 21,
    timezone="Asia/Shanghai",
    rules=GanzhiRules.bazi_default(),
)

cal.pillars.year.text   # 癸酉
cal.pillars.month.text  # 辛酉
cal.pillars.day.text    # 壬子
cal.pillars.hour.text   # 丁未
cal.previous_solar_term
cal.next_solar_term

pillars, trace = cal.ganzhi(explain=True)
# trace.year.reason 为确定性规则说明

term = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
```

时区**必填**。naive datetime 会抛出 `MissingTimezoneError`。

## CLI

| 命令 | 说明 |
|------|------|
| `convert` | 公/农历 → 历法快照 + 四柱 |
| `solar-term` | 二十四节气之一的精确时刻 |
| `version` | 包版本 |

### convert

| 选项 | 说明 |
|------|------|
| `--date` / `--lunar` | 公历或农历 `YYYY-MM-DD` |
| `--leap` | 将 `--lunar` 视为闰月 |
| `--time` | `HH:MM` 或 `HH:MM:SS` |
| `--timezone` | IANA 时区（**必填**） |
| `--profile` | `lunar`（默认）或 `bazi` |
| `--year-boundary` | 覆盖：`chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | 覆盖：`jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | 覆盖：`midnight` / `zi_start` |
| `--json` | 结构化 JSON |
| `--explain` | 附带确定性干支规则追溯 |

## 配置 / 规则

见 [docs/ganzhi-rules.md](docs/ganzhi-rules.md) 与 [docs/calendar-rules.md](docs/calendar-rules.md)。

## 示例

- [examples/python/basic.py](examples/python/basic.py)
- [examples/python/solar_terms.py](examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](examples/python/bazi_time_basis.py)

## 精度

见 [docs/accuracy.md](docs/accuracy.md)。支持公历年份：**1900–2100**。

## 路线图（摘要）

| 版本 | 重点 |
|------|------|
| 0.1.0a1 | 历法基础 |
| 0.1.0a2 | 二十四节气精确到秒 |
| 0.1.0a3 | 四柱 + explain（本版本） |
| 0.2+ | 自建天文核心；去掉运行时 sxtwl |
| 1.0 | 稳定 schema、权威 fixture、零运行时依赖 |


可选 `--envelope` 将结果包装为 `mystilink.envelope/0.1`（默认仍为裸 JSON）。

## 限制

- 尚未包含真太阳时 / 经度修正
- 节气时刻来自内部 provider（非观测台认证）
- 公开 API 不得 import 或暴露 `sxtwl`
- 本 alpha 未交付 Python 以外的语言矩阵绑定

## 许可

MIT。见 [LICENSE](LICENSE)。第三方运行时说明：[NOTICE](NOTICE)。

## 问题反馈

请附带：CLI 版本（`lunar version`）、完整命令行（仅使用虚构日期）、stdout/stderr。
