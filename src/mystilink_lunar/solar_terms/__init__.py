# -*- coding: utf-8 -*-
"""Solar-term lookup and adjacency."""
from __future__ import annotations

from datetime import datetime
from typing import Optional, Tuple

from mystilink_lunar.exceptions import UnknownSolarTermError
from mystilink_lunar.models import SolarTerm
from mystilink_lunar.providers import CalendarProvider, default_provider
from mystilink_lunar.solar_terms.definitions import resolve_solar_term_key, solar_term_def
from mystilink_lunar.timezone import require_aware, resolve_zone


def _term_from_index_dt(index: int, dt: datetime) -> SolarTerm:
    d = solar_term_def(index)
    return SolarTerm(
        index=d.index,
        id=d.id,
        name=d.name,
        chinese_name=d.chinese_name,
        solar_longitude=d.solar_longitude,
        datetime=dt,
    )


def get_solar_term(
    key: str | int,
    year: int,
    *,
    timezone: str,
    provider: Optional[CalendarProvider] = None,
) -> SolarTerm:
    """
    Exact instant of a solar term in the given Gregorian year.

    `key` may be an index (0–23, 冬至=0), id (`lichun` / `LICHUN`), or Chinese name.
    Returned datetime is timezone-aware in `timezone`.
    """
    try:
        definition = resolve_solar_term_key(key)
    except KeyError as exc:
        raise UnknownSolarTermError(str(exc)) from exc
    if not timezone:
        from mystilink_lunar.exceptions import MissingTimezoneError

        raise MissingTimezoneError("timezone is required (IANA name, e.g. Asia/Shanghai)")
    resolve_zone(timezone)  # validate early
    eng = provider or default_provider()
    instant = eng.solar_term_instant(definition.index, year, timezone=timezone)
    return _term_from_index_dt(definition.index, instant)


def adjacent_solar_terms(
    instant: datetime,
    *,
    provider: Optional[CalendarProvider] = None,
) -> Tuple[SolarTerm, SolarTerm]:
    """
    Previous term (datetime <= instant) and next term (datetime > instant).

    Instant must be timezone-aware; comparison uses that zone.
    """
    aware = require_aware(instant)
    eng = provider or default_provider()
    tz = aware.tzinfo
    assert tz is not None

    events: list[tuple[int, datetime]] = []
    for year in (aware.year - 1, aware.year, aware.year + 1):
        for index, shanghai in eng.solar_term_events(year):
            events.append((index, shanghai.astimezone(tz)))

    # Deduplicate by (index, iso datetime)
    uniq: dict[str, tuple[int, datetime]] = {}
    for index, dt in events:
        uniq[f"{index}:{dt.isoformat()}"] = (index, dt)
    ordered = sorted(uniq.values(), key=lambda item: item[1])

    previous: tuple[int, datetime] | None = None
    nxt: tuple[int, datetime] | None = None
    for index, dt in ordered:
        if dt <= aware:
            previous = (index, dt)
        elif nxt is None:
            nxt = (index, dt)
            break

    if previous is None or nxt is None:
        raise RuntimeError("failed to resolve adjacent solar terms near instant")

    return (
        _term_from_index_dt(previous[0], previous[1]),
        _term_from_index_dt(nxt[0], nxt[1]),
    )


def lichun_instant(
    year: int,
    *,
    timezone: str,
    provider: Optional[CalendarProvider] = None,
) -> datetime:
    return get_solar_term(3, year, timezone=timezone, provider=provider).datetime
