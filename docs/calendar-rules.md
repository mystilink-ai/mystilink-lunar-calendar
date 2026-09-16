# Calendar rules (alpha.3)

## Supported range

- Civil years **1900–2100** (provider window for this alpha)
- Conversion and solar-term instants use the internal `sxtwl` adapter; public APIs never expose `sxtwl`

## Solar ↔ lunar

- Lunar month day 1 is the civil date of the corresponding new-moon boundary as resolved by the provider
- `is_leap_month` marks intercalary months; leap months reuse the preceding month number

## 24 solar terms

- Index 0 = 冬至 … 23 = 大雪; 立春 = 3, apparent solar longitude 315°
- Instants are computed in China Standard Time (`Asia/Shanghai` wall clock from the provider) then converted to the requested IANA zone
- `get_solar_term(name, year, timezone=...)` returns the occurrence whose CST civil year equals `year`
- Snapshot fields: `previous_solar_term` (datetime ≤ instant), `next_solar_term` (datetime > instant)

## Year boundary (zodiac / year pillar)

| Value | Meaning | Status |
|-------|---------|--------|
| `chunjie` | Lunar New Year (正月初一) | Implemented |
| `lichun_day` | Civil date of Li Chun in the instant's zone | Implemented |
| `lichun_exact` | Exact Li Chun instant | Implemented |

Default profile: `GanzhiRules.lunar_calendar()`.  
BaZi profile: `GanzhiRules.bazi_default()` (`lichun_exact` + `jie_exact` + `zi_start`).

See [ganzhi-rules.md](ganzhi-rules.md) for month / day / hour pillars.

## Timezone

- All instants must be timezone-aware
- Conversion uses the **local civil date** in the given IANA zone
- Omitting timezone raises `MissingTimezoneError` (no silent Beijing default)
