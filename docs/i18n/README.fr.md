# Mystilink Calendrier lunaire

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Aperçu

Fondation déterministe et sensible au fuseau horaire pour le calendrier lunaire chinois et le cycle sexagésimal, destinée aux moteurs métaphysiques et aux outils d’agents. Ce paquet convertit les dates grégoriennes ↔ lunaires (y compris les mois intercalaires), expose les 24 termes solaires à la seconde, calcule les quatre piliers sous des règles explicites et renvoie du JSON structuré.

**v0.1.0a3 (Quatre piliers)** ajoute les piliers mois/jour/heure, les profils `GanzhiRules` et les traces de règles `ganzhi(explain=True)` au-dessus des termes solaires d’alpha.2.

## Plateformes et langages

| Cible | Livraison (alpha.3) |
|-------|---------------------|
| Python 3.10+ | Paquet installable `mystilink-lunar`, CLI `lunar` (alias `mystilink-lunar`) |
| C / C++ / C# / Java / JavaScript·Node | Prévu : liaisons légères au-dessus du JSON CLI |

## Prérequis

- Python 3.10 ou plus récent
- Fournisseur d’exécution : `sxtwl` (dépendance déclarée ; hors surface d’import publique)

## Installation et démarrage rapide

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

## API Python

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

Le fuseau horaire est **obligatoire**. Les datetime naïfs lèvent `MissingTimezoneError`.

## CLI

| Commande | Description |
|----------|-------------|
| `convert` | Solaire/lunaire → instantané calendaire + quatre piliers |
| `solar-term` | Instant exact d’un des 24 termes |
| `version` | Version du paquet |

### convert

| Option | Description |
|--------|-------------|
| `--date` / `--lunar` | Grégorien ou lunaire `YYYY-MM-DD` |
| `--leap` | Traiter `--lunar` comme mois intercalaire |
| `--time` | `HH:MM` ou `HH:MM:SS` |
| `--timezone` | Zone IANA (**obligatoire**) |
| `--profile` | `lunar` (défaut) ou `bazi` |
| `--year-boundary` | Remplacer : `chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | Remplacer : `jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | Remplacer : `midnight` / `zi_start` |
| `--json` | JSON structuré |
| `--explain` | Joindre des traces ganzhi déterministes |

## Configuration / règles

Voir [docs/ganzhi-rules.md](../ganzhi-rules.md) et [docs/calendar-rules.md](../calendar-rules.md).

## Exemples

- [examples/python/basic.py](../../examples/python/basic.py)
- [examples/python/solar_terms.py](../../examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](../../examples/python/bazi_time_basis.py)

## Précision

Voir [docs/accuracy.md](../accuracy.md). Années civiles prises en charge : **1900–2100**.

## Feuille de route (résumé)

| Version | Focus |
|---------|--------|
| 0.1.0a1 | Fondation calendaire |
| 0.1.0a2 | 24 termes solaires à la seconde |
| 0.1.0a3 | Quatre piliers + explain (cette version) |
| 0.2+ | Astronomie native ; retrait de sxtwl à l’exécution |
| 1.0 | Schéma stable, fixtures validées, zéro dépendance d’exécution |

L’option `--envelope` enveloppe le résultat en `mystilink.envelope/0.1` (par défaut : JSON nu).

## Limites

- Temps solaire vrai / correction de longitude non inclus pour l’instant
- Les horodatages des termes solaires suivent le fournisseur interne (non certifiés observatoire)
- Les API publiques ne doivent pas importer ni exposer `sxtwl`
- Les liaisons de la matrice linguistique hors Python ne sont pas livrées dans cet alpha

## Licence

MIT. Voir [LICENSE](../../LICENSE). Avis d’exécution tiers : [NOTICE](../../NOTICE).

## Retours

Signalez les défauts avec : version CLI (`lunar version`), ligne de commande exacte (dates fictives uniquement), et stdout/stderr.
