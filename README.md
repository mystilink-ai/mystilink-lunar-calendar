# Mystilink Lunar Calendar

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## Overview

Deterministic, timezone-aware Chinese lunar calendar and sexagenary-cycle foundation for metaphysics engines and agent tooling. This package converts Gregorian ↔ lunar dates (including leap months), exposes 24 solar terms to the second, computes four pillars under explicit rules, and returns structured JSON.

**v0.1.0a3 (Four Pillars)** adds month/day/hour pillars, `GanzhiRules` profiles, and `ganzhi(explain=True)` rule traces on top of alpha.2 solar terms.

## Platforms and languages

| Target | Delivery (alpha.3) |
|--------|--------------------|
| Python 3.10+ | Installable package `mystilink-lunar`, CLI `lunar` (alias `mystilink-lunar`) |
| C / C++ / C# / Java / JavaScript·Node | Planned: thin bindings over CLI JSON |

## Requirements

- Python 3.10 or newer
- Runtime provider: `sxtwl` (declared dependency; not part of the public import surface)

## Install and quick start

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

Timezone is **required**. Naive datetimes raise `MissingTimezoneError`.

## CLI

| Command | Description |
|---------|-------------|
| `convert` | Solar/lunar → calendar snapshot + four pillars |
| `solar-term` | Exact instant of one of the 24 terms |
| `version` | Package version |

### convert

| Option | Description |
|--------|-------------|
| `--date` / `--lunar` | Gregorian or lunar `YYYY-MM-DD` |
| `--leap` | Treat `--lunar` as leap month |
| `--time` | `HH:MM` or `HH:MM:SS` |
| `--timezone` | IANA zone (**required**) |
| `--profile` | `lunar` (default) or `bazi` |
| `--year-boundary` | Override: `chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | Override: `jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | Override: `midnight` / `zi_start` |
| `--json` | Structured JSON |
| `--explain` | Attach deterministic ganzhi traces |

## Configuration / rules

See [docs/ganzhi-rules.md](docs/ganzhi-rules.md) and [docs/calendar-rules.md](docs/calendar-rules.md).

## Examples

- [examples/python/basic.py](examples/python/basic.py)
- [examples/python/solar_terms.py](examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](examples/python/bazi_time_basis.py)

## Accuracy

See [docs/accuracy.md](docs/accuracy.md). Supported civil years: **1900–2100**.

## Roadmap (summary)

| Version | Focus |
|---------|--------|
| 0.1.0a1 | Calendar foundation |
| 0.1.0a2 | 24 solar terms to the second |
| 0.1.0a3 | Four pillars + explain (this release) |
| 0.2+ | Native astronomy; retire runtime sxtwl |
| 1.0 | Stable schema, validated fixtures, zero runtime deps |

## Limits

- True solar time / longitude correction not included yet
- Solar-term timestamps follow the internal provider (not observatory-certified)
- Public APIs must not import or expose `sxtwl`
- Language-matrix bindings beyond Python are not shipped in this alpha

## License

MIT. See [LICENSE](LICENSE). Third-party runtime notice: [NOTICE](NOTICE).

## Feedback

Report defects with: CLI version (`lunar version`), exact command line (fictional dates only), and stdout/stderr.
