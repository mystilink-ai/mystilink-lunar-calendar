# Accuracy & validation

## Alpha.3 status

- Conversion / leap months / solar terms: internal `sxtwl` provider
- Four pillars: Mystilink rule layer (五虎遁 / 五鼠遁 / day epoch / jie adjacency)
- Cross-checks: 1993-09-28 pillars, 立秋 ±1 s month change, 子时 22:59/23:00/00:00/01:00, Li Chun year boundaries

Provider solar-term timestamps can differ from published almanacs by seconds.

## Planned oracles (later)

- sxtwl / lunar-python contrast (tests only)
- GB/T 33661-2017 rule assertions
- Observatory solar-term samples

## Fixture checklist

- [x] Ordinary date `1993-09-28`
- [x] Lunar New Year boundary
- [x] Leap month
- [x] Li Chun ±1 second
- [x] Jing Zhe ±1 second
- [x] Li Qiu ±1 second (month pillar)
- [x] 子时 edges 22:59 / 23:00 / 00:00 / 01:00
- [x] Multi-zone Li Chun conversion
