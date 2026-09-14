# -*- coding: utf-8 -*-
"""Internal calendar providers."""
from __future__ import annotations

from mystilink_lunar.providers.base import CalendarProvider
from mystilink_lunar.providers.sxtwl import SxtwlProvider

__all__ = ["CalendarProvider", "SxtwlProvider", "default_provider"]


def default_provider() -> CalendarProvider:
    return SxtwlProvider()
