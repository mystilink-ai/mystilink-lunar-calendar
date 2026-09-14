# Ganzhi rules (alpha.1)

## Year pillar

Computed from the **lunar year number** when `year_boundary="chunjie"`:

```text
stem_index   = (year - 4) % 10
branch_index = (year - 4) % 12
```

Zodiac follows `branch_index`.

## Not in alpha.1

- Month pillar (`jie_exact` / lunar month)
- Day pillar
- Hour pillar (`double_hour`, early/late 子)
- `explain=True` rule traces
- `lichun_day` / `lichun_exact` year boundaries
