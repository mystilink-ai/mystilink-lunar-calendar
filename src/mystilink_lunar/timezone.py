# -*- coding: utf-8 -*-
"""Timezone helpers: naive datetimes are rejected."""
from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mystilink_lunar.exceptions import InvalidTimezoneError, MissingTimezoneError


def resolve_zone(timezone: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise InvalidTimezoneError(f"Unknown IANA timezone: {timezone!r}") from exc


def require_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        raise MissingTimezoneError(
            "datetime must be timezone-aware; pass timezone= or an aware datetime"
        )
    return dt


def build_aware_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    *,
    timezone: str,
) -> datetime:
    if not timezone:
        raise MissingTimezoneError("timezone is required (IANA name, e.g. Asia/Shanghai)")
    tz = resolve_zone(timezone)
    return datetime(year, month, day, hour, minute, second, tzinfo=tz)


def civil_date_in_zone(dt: datetime) -> date:
    aware = require_aware(dt)
    return aware.date()


def combine_civil(d: date, t: time, timezone: str) -> datetime:
    tz = resolve_zone(timezone)
    return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, tzinfo=tz)
