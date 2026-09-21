# Mystilink Calendario lunar

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Resumen

Base determinista y con zona horaria del calendario lunar chino y del ciclo sexagenario para motores metafísicos y herramientas de agente. Este paquete convierte fechas gregorianas ↔ lunares (incluidos meses intercalares), expone los 24 términos solares al segundo, calcula los cuatro pilares bajo reglas explícitas y devuelve JSON estructurado.

**v0.1.0a3 (Cuatro pilares)** añade pilares de mes/día/hora, perfiles `GanzhiRules` y trazas de reglas `ganzhi(explain=True)` sobre los términos solares de alpha.2.

## Plataformas e idiomas

| Objetivo | Entrega (alpha.3) |
|----------|-------------------|
| Python 3.10+ | Paquete instalable `mystilink-lunar`, CLI `lunar` (alias `mystilink-lunar`) |
| C / C++ / C# / Java / JavaScript·Node | Planificado: enlaces ligeros sobre JSON del CLI |

## Requisitos

- Python 3.10 o superior
- Proveedor en tiempo de ejecución: `sxtwl` (dependencia declarada; no forma parte de la superficie de importación pública)

## Instalación e inicio rápido

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

## API de Python

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

La zona horaria es **obligatoria**. Los datetime ingenuos lanzan `MissingTimezoneError`.

## CLI

| Comando | Descripción |
|---------|-------------|
| `convert` | Solar/lunar → instantánea de calendario + cuatro pilares |
| `solar-term` | Instantánea exacta de uno de los 24 términos |
| `version` | Versión del paquete |

### convert

| Opción | Descripción |
|--------|-------------|
| `--date` / `--lunar` | Gregoriano o lunar `YYYY-MM-DD` |
| `--leap` | Tratar `--lunar` como mes intercalar |
| `--time` | `HH:MM` o `HH:MM:SS` |
| `--timezone` | Zona IANA (**obligatoria**) |
| `--profile` | `lunar` (predeterminado) o `bazi` |
| `--year-boundary` | Anular: `chunjie` / `lichun_day` / `lichun_exact` |
| `--month-boundary` | Anular: `jie_exact` / `jie_day` / `lunar_month` |
| `--day-boundary` | Anular: `midnight` / `zi_start` |
| `--json` | JSON estructurado |
| `--explain` | Adjuntar trazas ganzhi deterministas |

## Configuración / reglas

Véase [docs/ganzhi-rules.md](../ganzhi-rules.md) y [docs/calendar-rules.md](../calendar-rules.md).

## Ejemplos

- [examples/python/basic.py](../../examples/python/basic.py)
- [examples/python/solar_terms.py](../../examples/python/solar_terms.py)
- [examples/python/bazi_time_basis.py](../../examples/python/bazi_time_basis.py)

## Precisión

Véase [docs/accuracy.md](../accuracy.md). Años civiles admitidos: **1900–2100**.

## Hoja de ruta (resumen)

| Versión | Enfoque |
|---------|---------|
| 0.1.0a1 | Base del calendario |
| 0.1.0a2 | 24 términos solares al segundo |
| 0.1.0a3 | Cuatro pilares + explain (esta versión) |
| 0.2+ | Astronomía nativa; retirar sxtwl en tiempo de ejecución |
| 1.0 | Esquema estable, fixtures validados, cero dependencias en tiempo de ejecución |

La opción `--envelope` envuelve el resultado como `mystilink.envelope/0.1` (por defecto sigue siendo JSON desnudo).

## Límites

- Aún no se incluye tiempo solar verdadero / corrección de longitud
- Las marcas de tiempo de los términos solares siguen el proveedor interno (no certificadas por observatorio)
- Las API públicas no deben importar ni exponer `sxtwl`
- Los enlaces de la matriz de lenguajes fuera de Python no se envían en este alpha

## Licencia

MIT. Véase [LICENSE](../../LICENSE). Aviso de tiempo de ejecución de terceros: [NOTICE](../../NOTICE).

## Comentarios

Informe defectos con: versión CLI (`lunar version`), línea de comando exacta (solo fechas ficticias) y stdout/stderr.
