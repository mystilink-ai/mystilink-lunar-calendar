# Mystilink Lunar Calendar

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## Overview

Deterministic, timezone-aware Chinese lunar calendar and sexagenary-cycle foundation for metaphysics engines and agent tooling. This package converts Gregorian ↔ lunar dates (including leap months), exposes structured JSON, and keeps calendar facts separate from BaZi / Zi Wei rule engines.

**v0.1.0a1 (Calendar Foundation)** includes solar↔lunar, leap months, required IANA timezone, year ganzhi + zodiac (`chunjie` boundary), `to_dict()`, and CLI `convert`. Solar terms and full four pillars arrive in later alphas.

## Platforms and languages

| Target | Delivery (alpha.1) |
|--------|--------------------|
| Python 3.10+ | Installable package `mystilink-lunar`, CLI `mystilink-lunar` |
| C / C++ / C# / Java / JavaScript·Node | Planned: thin bindings over CLI JSON (same pattern as sibling calculators) |

## Requirements

- Python 3.10 or newer
- Runtime provider: `sxtwl` (declared dependency; not part of the public import surface)

## Install and quick start

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

Also:

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
cal.to_dict()      # structured dict / JSON-ready
```

Timezone is **required**. Naive datetimes raise `MissingTimezoneError`.

Lunar → Gregorian:

```python
cal = LunarCalendar.from_lunar(
    2023, 2, 1,
    is_leap_month=True,
    timezone="Asia/Shanghai",
)
```

## CLI

| Command | Description |
|---------|-------------|
| `convert` | Solar or lunar input → calendar snapshot |
| `version` | Package version |

### convert

| Option | Description |
|--------|-------------|
| `--date` | Gregorian `YYYY-MM-DD` |
| `--lunar` | Lunar `YYYY-MM-DD` |
| `--leap` | Treat `--lunar` as leap month |
| `--time` | `HH:MM` or `HH:MM:SS` (default `00:00:00`) |
| `--timezone` | IANA zone (**required**) |
| `--year-boundary` | `chunjie` (default; only implemented boundary in alpha.1) |
| `--json` | Print JSON matching `schema/convert.output.json` |

## Configuration / rules

- `GanzhiRules.year_boundary`: `chunjie` | `lichun_day` | `lichun_exact`
- Alpha.1 implements `chunjie` only; other values raise until solar terms land
- Details: [docs/calendar-rules.md](docs/calendar-rules.md)

## Examples

- [examples/python/basic.py](examples/python/basic.py)

## Accuracy

See [docs/accuracy.md](docs/accuracy.md). Supported civil years for this alpha: **1900–2100**.

## Roadmap (summary)

| Version | Focus |
|---------|--------|
| 0.1.0a1 | Calendar foundation (this release) |
| alpha.2 | 24 solar terms to the second |
| alpha.3 | Ganzhi four pillars + rule explain |
| 0.2+ | Native astronomy; retire runtime sxtwl |
| 1.0 | Stable schema, validated fixtures, zero runtime deps |

## Limits

- Month / day / hour pillars and solar-term objects are not computed yet
- Year boundary other than `chunjie` is not available
- Public APIs must not import or expose `sxtwl`
- Language-matrix bindings beyond Python are not shipped in alpha.1

## License

MIT. See [LICENSE](LICENSE). Third-party runtime notice: [NOTICE](NOTICE).

## Feedback

Report defects with: CLI version (`mystilink-lunar version`), exact command line (fictional dates only), and stdout/stderr.
