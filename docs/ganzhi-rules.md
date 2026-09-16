# Ganzhi rules (alpha.3)

## Profiles

| Profile | year | month | day | hour |
|---------|------|-------|-----|------|
| `GanzhiRules.lunar_calendar()` | `chunjie` | `lunar_month` | `midnight` | `double_hour` |
| `GanzhiRules.bazi_default()` | `lichun_exact` | `jie_exact` | `zi_start` | `double_hour` |

## Year pillar

```text
stem_index   = (year_num - 4) % 10
branch_index = (year_num - 4) % 12
```

| Boundary | `year_num` |
|----------|------------|
| `chunjie` | Lunar year of the civil date |
| `lichun_day` | `Y` if local date ≥ Li Chun date in `Y`, else `Y - 1` |
| `lichun_exact` | `Y` if instant ≥ Li Chun instant in `Y`, else `Y - 1` |

Zodiac follows the year branch.

## Month pillar

| Boundary | Rule |
|----------|------|
| `lunar_month` | Lunar month `N` → branch `(N + 1) mod 12` (正月→寅); leap months keep `N` |
| `jie_exact` | Previous **节** with `datetime <= instant` |
| `jie_day` | Previous **节** with civil date ≤ local date |

Month stem via 五虎遁 from the year stem.

节 → branch: 小寒丑 … 立春寅 … 大雪子.

## Day pillar

Epoch verified against samples: **1900-01-31 = 甲辰**.

```text
days = civil_date - 1900-01-31
stem_index   = days % 10
branch_index = (days + 4) % 12
```

| Boundary | Civil date used |
|----------|-----------------|
| `midnight` | Local calendar date |
| `zi_start` | Local date + 1 day when `hour >= 23` |

## Hour pillar

`double_hour` 时辰: `((hour*60 + minute + 60) % 1440) // 120` → branch index 0=子 … 11=亥.

Hour stem via 五鼠遁 from the **day** stem (after day-boundary resolution).

## Explain

`cal.ganzhi(explain=True)` returns deterministic `PillarTrace` reasons (boundary + inputs), not model-generated prose.
