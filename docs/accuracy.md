# Accuracy & validation

## Alpha.1 status

- Conversion and leap months: delegated to the internal `sxtwl` provider
- Cross-checks: unit fixtures for 1993-09-28, 1993 Spring Festival ±1 day, 2023 leap month
- Solar-term timestamps: not yet shipped (`solar_term` is `null` in JSON)

## Planned oracles (later alphas)

- sxtwl (runtime provider → test-only)
- lunar-python (behavior contrast, tests only)
- GB/T 33661-2017 rule assertions
- Published almanac / observatory solar-term samples

## Fixture checklist (growing)

- [x] Ordinary date `1993-09-28`
- [x] Lunar New Year boundary (1993-01-22 / 1993-01-23)
- [x] Leap month (2023 leap 二月)
- [ ] Li Chun ±1 second
- [ ] Jieqi month boundaries
- [ ] 子时 hour edges
- [ ] Multi-zone same civil wall time
