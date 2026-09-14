# Changelog

## 0.1.0a1 — Calendar Foundation

- Solar ↔ lunar conversion (leap months included)
- Timezone-aware API (`MissingTimezoneError` when timezone is missing)
- Year ganzhi + zodiac with explicit `year_boundary` (`chunjie` for this alpha)
- `to_dict()` / JSON Schema draft
- CLI: `mystilink-lunar convert` (human text or `--json`)
- Internal sxtwl provider (not re-exported)
