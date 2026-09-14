# Contributing (technical)

## Setup

```bash
python3 -m pip install -e ".[dev]"
pytest
```

## Scope

- Keep this package a **calendar foundation** (conversion, solar terms, ganzhi rules, JSON)
- Do not add ten gods, shensha, almanac taboos, or chart interpretation
- Public imports must not expose `sxtwl`

## Tests

Add fixtures for boundary cases (Spring Festival, leap months, later: solar-term ±1s). Use fictional personal data only.

## License

Contributions are under MIT. Preserve `NOTICE` for third-party requirements.
