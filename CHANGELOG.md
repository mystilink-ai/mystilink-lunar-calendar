# Changelog

## 0.1.0a5

- CLI `convert --envelope` / `--locale` wraps convert JSON as mystilink.envelope/0.1
- Default human / `--json` output unchanged when `--envelope` is omitted

## 0.1.0a4

- Primary CLI entry point is `lunar`; alias `mystilink-lunar` remains installed


## 0.1.0a3 — Four Pillars

- Year / month / day / hour pillars with explicit `GanzhiRules`
- Profiles: `lunar_calendar()` and `bazi_default()`
- `cal.ganzhi(explain=True)` deterministic rule traces
- CLI: `--profile`, `--month-boundary`, `--day-boundary`, `--explain`

## 0.1.0a2 — Solar Terms

- 24 solar terms to the second (`get_solar_term`, previous/next on snapshots)
- Year boundaries `lichun_day` and `lichun_exact`
- CLI: `mystilink-lunar solar-term`
- JSON `solar_term.previous` / `solar_term.next`

## 0.1.0a1 — Calendar Foundation

- Solar ↔ lunar conversion (leap months included)
- Timezone-aware API (`MissingTimezoneError` when timezone is missing)
- Year ganzhi + zodiac with explicit `year_boundary` (`chunjie` for this alpha)
- `to_dict()` / JSON Schema draft
- CLI: `mystilink-lunar convert` (human text or `--json`)
- Internal sxtwl provider (not re-exported)
