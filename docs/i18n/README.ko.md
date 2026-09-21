# Mystilink 음력 달력

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

형이상학 엔진과 에이전트 도구를 위한 결정적·타임존 인식 중국 음력 및 육십갑자 기반 라이브러리입니다. 그레고리력 ↔ 음력(윤달 포함) 변환, 24절기 초 단위 시각, 명시적 규칙 하의 사주 계산, 구조화 JSON 출력을 제공합니다.

**v0.1.0a3(사주)** 는 alpha.2 절기 기능 위에 월/일/시주, `GanzhiRules` 프로필, `ganzhi(explain=True)` 규칙 추적을 추가합니다.

## 플랫폼 및 언어

| 대상 | 제공물(alpha.3) |
|------|-----------------|
| Python 3.10+ | 설치 가능 패키지 `mystilink-lunar`, CLI `lunar`(별칭 `mystilink-lunar`) |
| C / C++ / C# / Java / JavaScript·Node | 예정: CLI JSON 위의 얇은 바인딩 |

## 요구 사항

- Python 3.10 이상
- 런타임 프로바이더: `sxtwl`(의존성으로 선언; 공개 import 표면에 포함되지 않음)

## 설치 및 빠른 시작

```bash
cd mystilink-lunar-calendar
python3 -m pip install -e ".[dev]"

lunar convert \
  --date 1993-09-28 \
  --time 13:21 \
  --timezone Asia/Shanghai \
  --profile bazi \
  --json
```

## Python API

```python
from mystilink_lunar import LunarCalendar, GanzhiRules, get_solar_term

cal = LunarCalendar.from_solar(
    1993, 9, 28, 13, 21,
    timezone="Asia/Shanghai",
    rules=GanzhiRules.bazi_default(),
)

cal.pillars.year.text   # 癸酉
cal.pillars.month.text  # 辛酉
cal.pillars.day.text    # 壬子
cal.pillars.hour.text   # 丁未
cal.previous_solar_term
cal.next_solar_term

pillars, trace = cal.ganzhi(explain=True)
# trace.year.reason is a deterministic rule string

term = get_solar_term("lichun", 2026, timezone="Asia/Shanghai")
```

타임존은 **필수**입니다. naive datetime 은 `MissingTimezoneError` 를 발생시킵니다.

## CLI

| 명령 | 설명 |
|------|------|
| `convert` | 양력/음력 → 달력 스냅샷 + 사주 |
| `solar-term` | 24절기 중 하나의 정확한 시각 |
| `version` | 패키지 버전 |

### convert

| 옵션 | 설명 |
|------|------|
| `--date` / `--lunar` | 그레고리력 또는 음력 `YYYY-MM-DD` |
| `--leap` | `--lunar` 를 윤달로 취급 |
| `--time` | `HH:MM` 또는 `HH:MM:SS` |
| `--timezone` | IANA 존(**필수**) |
| `--profile` | `lunar`(기본) 또는 `bazi` |
| `--year-boundary` | 덮어쓰기: `chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | 덮어쓰기: `jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | 덮어쓰기: `midnight` / `zi_start` |
| `--json` | 구조화 JSON |
| `--explain` | 결정적 간지 추적 첨부 |

## 구성 / 규칙

[docs/ganzhi-rules.md](../ganzhi-rules.md) 및 [docs/calendar-rules.md](../calendar-rules.md) 참조.

## 예제

- [examples/python/basic.py](../../examples/python/basic.py)
- [examples/python/solar_terms.py](../../examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](../../examples/python/bazi_time_basis.py)

## 정확도

[docs/accuracy.md](../accuracy.md) 참조. 지원 민간 연도: **1900–2100**.

## 로드맵(요약)

| 버전 | 초점 |
|------|------|
| 0.1.0a1 | 달력 기반 |
| 0.1.0a2 | 24절기 초 단위 |
| 0.1.0a3 | 사주 + explain(본 릴리스) |
| 0.2+ | 네이티브 천문; 런타임 sxtwl 제거 |
| 1.0 | 안정 schema, 검증 fixture, 런타임 의존성 제로 |

선택적 `--envelope` 는 결과를 `mystilink.envelope/0.1` 로 감쌉니다(기본은 원시 JSON).

## 제한

- 진태양시 / 경도 보정은 아직 미포함
- 절기 타임스탬프는 내부 프로바이더를 따름(관측소 인증 아님)
- 공개 API 는 `sxtwl` 을 import 하거나 노출해서는 안 됨
- 본 alpha 에서는 Python 외 언어 매트릭스 바인딩 미제공

## 라이선스

MIT. [LICENSE](../../LICENSE) 참조. 서드파티 런타임 고지: [NOTICE](../../NOTICE).

## 피드백

결함 보고 시 첨부: CLI 버전(`lunar version`), 정확한 명령줄(가상 날짜만), stdout/stderr.
