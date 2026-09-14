# -*- coding: utf-8 -*-
"""sxtwl-backed calendar provider (not part of the public API surface)."""
from __future__ import annotations

from mystilink_lunar.exceptions import DateOutOfRangeError, InvalidLunarDateError, ProviderError
from mystilink_lunar.models import LunarDate, SolarDate

# Practical validation window for alpha; sxtwl itself supports a wider range.
_MIN_YEAR = 1900
_MAX_YEAR = 2100


class SxtwlProvider:
    """Adapter around the sxtwl PyPI package."""

    name = "sxtwl"

    def __init__(self) -> None:
        try:
            import sxtwl  # noqa: F401
        except ImportError as exc:
            raise ProviderError(
                "sxtwl is required for the default provider; install mystilink-lunar"
            ) from exc

    def solar_to_lunar(self, solar: SolarDate) -> LunarDate:
        self._check_solar(solar)
        import sxtwl

        try:
            day = sxtwl.fromSolar(solar.year, solar.month, solar.day)
        except Exception as exc:  # noqa: BLE001 — SWIG raises varied types
            raise ProviderError(f"sxtwl.fromSolar failed: {exc}") from exc
        return LunarDate(
            year=int(day.getLunarYear()),
            month=int(day.getLunarMonth()),
            day=int(day.getLunarDay()),
            is_leap_month=bool(day.isLunarLeap()),
        )

    def lunar_to_solar(self, lunar: LunarDate) -> SolarDate:
        if not 1 <= lunar.month <= 12:
            raise InvalidLunarDateError(f"lunar month out of range: {lunar.month}")
        if not 1 <= lunar.day <= 30:
            raise InvalidLunarDateError(f"lunar day out of range: {lunar.day}")
        if not _MIN_YEAR <= lunar.year <= _MAX_YEAR:
            raise DateOutOfRangeError(
                f"lunar year {lunar.year} outside supported range {_MIN_YEAR}-{_MAX_YEAR}"
            )
        import sxtwl

        try:
            day = sxtwl.fromLunar(
                lunar.year, lunar.month, lunar.day, bool(lunar.is_leap_month)
            )
        except Exception as exc:  # noqa: BLE001
            raise InvalidLunarDateError(
                f"invalid lunar date {lunar.year}-{lunar.month}-{lunar.day} "
                f"leap={lunar.is_leap_month}: {exc}"
            ) from exc
        return SolarDate(
            year=int(day.getSolarYear()),
            month=int(day.getSolarMonth()),
            day=int(day.getSolarDay()),
        )

    def _check_solar(self, solar: SolarDate) -> None:
        if not _MIN_YEAR <= solar.year <= _MAX_YEAR:
            raise DateOutOfRangeError(
                f"solar year {solar.year} outside supported range {_MIN_YEAR}-{_MAX_YEAR}"
            )
        if not 1 <= solar.month <= 12:
            raise DateOutOfRangeError(f"solar month out of range: {solar.month}")
        if not 1 <= solar.day <= 31:
            raise DateOutOfRangeError(f"solar day out of range: {solar.day}")
