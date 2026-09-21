# Mystilink 旧暦カレンダー

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

形而上学エンジンおよびエージェント向けの、決定論的・タイムゾーン対応の中国旧暦および六十干支の基盤ライブラリです。グレゴリオ暦 ↔ 旧暦（閏月を含む）の変換、24節気の秒精度、明示的ルールに基づく四柱計算、構造化 JSON の出力を提供します。

**v0.1.0a3（四柱）** は、alpha.2 の節気機能に加え、月/日/時柱、`GanzhiRules` プロファイル、および `ganzhi(explain=True)` によるルール追跡を追加します。

## プラットフォームと言語

| 対象 | 提供物（alpha.3） |
|------|-------------------|
| Python 3.10+ | インストール可能なパッケージ `mystilink-lunar`、CLI `lunar`（別名 `mystilink-lunar`） |
| C / C++ / C# / Java / JavaScript·Node | 予定：CLI JSON 上の薄いバインディング |

## 要件

- Python 3.10 以降
- ランタイムプロバイダ：`sxtwl`（依存関係として宣言；公開 import 面には含めない）

## インストールとクイックスタート

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

タイムゾーンは**必須**です。naive datetime は `MissingTimezoneError` を送出します。

## CLI

| コマンド | 説明 |
|---------|------|
| `convert` | 太陽暦/旧暦 → カレンダースナップショット + 四柱 |
| `solar-term` | 24節気のうち1つの正確な時刻 |
| `version` | パッケージバージョン |

### convert

| オプション | 説明 |
|-----------|------|
| `--date` / `--lunar` | グレゴリオ暦または旧暦 `YYYY-MM-DD` |
| `--leap` | `--lunar` を閏月として扱う |
| `--time` | `HH:MM` または `HH:MM:SS` |
| `--timezone` | IANA ゾーン（**必須**） |
| `--profile` | `lunar`（デフォルト）または `bazi` |
| `--year-boundary` | 上書き：`chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | 上書き：`jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | 上書き：`midnight` / `zi_start` |
| `--json` | 構造化 JSON |
| `--explain` | 決定論的な干支トレースを付与 |

## 設定 / ルール

[docs/ganzhi-rules.md](../ganzhi-rules.md) および [docs/calendar-rules.md](../calendar-rules.md) を参照。

## 例

- [examples/python/basic.py](../../examples/python/basic.py)
- [examples/python/solar_terms.py](../../examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](../../examples/python/bazi_time_basis.py)

## 精度

[docs/accuracy.md](../accuracy.md) を参照。対応する民用年：**1900–2100**。

## ロードマップ（要約）

| バージョン | 焦点 |
|-----------|------|
| 0.1.0a1 | カレンダー基盤 |
| 0.1.0a2 | 24節気の秒精度 |
| 0.1.0a3 | 四柱 + explain（本リリース） |
| 0.2+ | ネイティブ天文学；ランタイム sxtwl の廃止 |
| 1.0 | 安定 schema、検証済み fixture、ランタイム依存ゼロ |

任意の `--envelope` は結果を `mystilink.envelope/0.1` で包みます（デフォルトは裸の JSON）。

## 制限

- 真太陽時 / 経度補正は未対応
- 節気タイムスタンプは内部プロバイダに従う（観測所認証ではない）
- 公開 API は `sxtwl` を import または公開してはならない
- 本 alpha では Python 以外の言語マトリクスバインディングは未同梱

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。サードパーティランタイム通知：[NOTICE](../../NOTICE)。

## フィードバック

不具合報告時は次を添付：CLI バージョン（`lunar version`）、正確なコマンドライン（架空の日付のみ）、stdout/stderr。
