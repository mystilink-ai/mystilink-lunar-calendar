# Calendar rules (alpha.1)

## Supported range

- Civil years **1900–2100** (provider window for this alpha)
- Conversion uses the internal `sxtwl` adapter; public APIs never expose `sxtwl`

## Solar ↔ lunar

- Lunar month day 1 is the civil date of the corresponding new-moon boundary as resolved by the provider
- `is_leap_month` marks intercalary months; leap months reuse the preceding month number

## Year boundary (zodiac / year pillar)

| Value | Meaning | Alpha.1 |
|-------|---------|---------|
| `chunjie` | Lunar New Year (正月初一) | Implemented |
| `lichun_day` | Li Chun civil day | Planned (alpha.2+) |
| `lichun_exact` | Li Chun exact instant | Planned (alpha.2+) |

Default profile: `GanzhiRules.lunar_calendar()` → `chunjie`.

## Timezone

- All instants must be timezone-aware
- Conversion uses the **local civil date** in the given IANA zone
- Omitting timezone raises `MissingTimezoneError` (no silent Beijing default)
