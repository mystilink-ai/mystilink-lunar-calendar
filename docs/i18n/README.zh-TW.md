# Mystilink 農曆曆法庫

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

面向術數引擎與 Agent 工具的確定性、時區感知中國農曆與干支基礎庫。提供公曆 ↔ 農曆（含閏月）、二十四節氣精確到秒、在明示規則下計算四柱，並輸出結構化 JSON。

**v0.1.0a3（四柱）** 在 alpha.2 節氣能力之上，增加月/日/時柱、`GanzhiRules` 配置檔，以及 `ganzhi(explain=True)` 規則追溯。

## 平台與語言

| 目標 | 交付（alpha.3） |
|------|-----------------|
| Python 3.10+ | 可安裝套件 `mystilink-lunar`，CLI `lunar`（別名 `mystilink-lunar`） |
| C / C++ / C# / Java / JavaScript·Node | 計劃：基於 CLI JSON 的薄綁定 |

## 環境需求

- Python 3.10 或更高
- 執行時期 provider：`sxtwl`（已寫入相依性；不出現在公開 import 面）

## 安裝與快速開始

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
# trace.year.reason is a deterministic rule string

term = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
```

時區**必填**。naive datetime 會拋出 `MissingTimezoneError`。

## CLI

| 命令 | 說明 |
|------|------|
| `convert` | 公/農曆 → 曆法快照 + 四柱 |
| `solar-term` | 二十四節氣之一的精確時刻 |
| `version` | 套件版本 |

### convert

| 選項 | 說明 |
|------|------|
| `--date` / `--lunar` | 公曆或農曆 `YYYY-MM-DD` |
| `--leap` | 將 `--lunar` 視為閏月 |
| `--time` | `HH:MM` 或 `HH:MM:SS` |
| `--timezone` | IANA 時區（**必填**） |
| `--profile` | `lunar`（預設）或 `bazi` |
| `--year-boundary` | 覆寫：`chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | 覆寫：`jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | 覆寫：`midnight` / `zi_start` |
| `--json` | 結構化 JSON |
| `--explain` | 附帶確定性干支規則追溯 |

## 設定 / 規則

見 [docs/ganzhi-rules.md](../ganzhi-rules.md) 與 [docs/calendar-rules.md](../calendar-rules.md)。

## 範例

- [examples/python/basic.py](../../examples/python/basic.py)
- [examples/python/solar_terms.py](../../examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](../../examples/python/bazi_time_basis.py)

## 精度

見 [docs/accuracy.md](../accuracy.md)。支援公曆年份：**1900–2100**。

## 路線圖（摘要）

| 版本 | 重點 |
|------|------|
| 0.1.0a1 | 曆法基礎 |
| 0.1.0a2 | 二十四節氣精確到秒 |
| 0.1.0a3 | 四柱 + explain（本版本） |
| 0.2+ | 自建天文核心；去掉執行時期 sxtwl |
| 1.0 | 穩定 schema、權威 fixture、零執行時期相依 |

可選 `--envelope` 將結果包裝為 `mystilink.envelope/0.1`（預設仍為裸 JSON）。

## 限制

- 尚未包含真太陽時 / 經度修正
- 節氣時刻來自內部 provider（非觀測台認證）
- 公開 API 不得 import 或暴露 `sxtwl`
- 本 alpha 未交付 Python 以外的語言矩陣綁定

## 授權

MIT。見 [LICENSE](../../LICENSE)。第三方執行時期說明：[NOTICE](../../NOTICE)。

## 問題回報

請附帶：CLI 版本（`lunar version`）、完整命令列（僅使用虛構日期）、stdout/stderr。
