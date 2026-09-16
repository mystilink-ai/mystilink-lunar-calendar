# -*- coding: utf-8 -*-
"""Public exceptions."""
from __future__ import annotations


class MystilinkLunarError(Exception):
    """Base error for mystilink-lunar."""


class MissingTimezoneError(MystilinkLunarError):
    """Raised when a timezone-aware instant is required but missing."""


class InvalidTimezoneError(MystilinkLunarError):
    """Raised when an IANA timezone name cannot be resolved."""


class DateOutOfRangeError(MystilinkLunarError):
    """Raised when the civil date is outside the supported provider range."""


class InvalidLunarDateError(MystilinkLunarError):
    """Raised when a lunar year/month/day (or leap flag) is invalid."""


class ProviderError(MystilinkLunarError):
    """Raised when the internal calendar provider fails."""


class UnknownSolarTermError(MystilinkLunarError):
    """Raised when a solar-term name or index cannot be resolved."""


class SolarTermNotFoundError(MystilinkLunarError):
    """Raised when a solar term cannot be located for the requested year."""
