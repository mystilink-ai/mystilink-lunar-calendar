# -*- coding: utf-8 -*-
"""CLI for Mystilink lunar calendar."""
from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Optional

from mystilink_lunar.calendar import LunarCalendar
from mystilink_lunar.exceptions import MystilinkLunarError
from mystilink_lunar.models import GanzhiRules

PACKAGE_NAME = "mystilink-lunar"
FALLBACK_VERSION = "0.1.0a1"


def get_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return FALLBACK_VERSION


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _print_error(message: str, code: int = 1) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def _parse_time(value: Optional[str]) -> tuple[int, int, int]:
    if not value:
        return 0, 0, 0
    parts = value.split(":")
    if len(parts) not in (2, 3):
        raise ValueError("time must be HH:MM or HH:MM:SS")
    hour = int(parts[0])
    minute = int(parts[1])
    second = int(parts[2]) if len(parts) == 3 else 0
    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError("time out of range")
    return hour, minute, second


def _parse_date(value: str) -> tuple[int, int, int]:
    parts = value.split("-")
    if len(parts) != 3:
        raise ValueError("date must be YYYY-MM-DD")
    return int(parts[0]), int(parts[1]), int(parts[2])


def _human(cal: LunarCalendar) -> str:
    lunar = cal.lunar
    leap = " leap" if lunar.is_leap_month else ""
    lines = [
        f"Solar       {cal.instant.isoformat()}",
        f"Timezone    {cal.timezone}",
        f"Lunar       {lunar.year}-{lunar.month:02d}-{lunar.day:02d}{leap}",
        f"Year        {cal.year_ganzhi.text}",
        f"Zodiac      {cal.zodiac.id} ({cal.zodiac.chinese})",
        f"Boundary    {cal.rules.year_boundary}",
        f"Provider    {cal.provider_name}",
    ]
    return "\n".join(lines)


def cmd_convert(args: argparse.Namespace) -> None:
    if not args.timezone:
        _print_error("timezone is required (IANA name, e.g. Asia/Shanghai)")
    try:
        hour, minute, second = _parse_time(args.time)
        rules = GanzhiRules(year_boundary=args.year_boundary)
        if args.lunar:
            y, m, d = _parse_date(args.lunar)
            cal = LunarCalendar.from_lunar(
                y,
                m,
                d,
                is_leap_month=bool(args.leap),
                hour=hour,
                minute=minute,
                second=second,
                timezone=args.timezone,
                rules=rules,
            )
        else:
            if not args.date:
                _print_error("provide --date YYYY-MM-DD or --lunar YYYY-MM-DD")
            y, m, d = _parse_date(args.date)
            cal = LunarCalendar.from_solar(
                y,
                m,
                d,
                hour,
                minute,
                second,
                timezone=args.timezone,
                rules=rules,
            )
    except MystilinkLunarError as exc:
        _print_error(str(exc))
    except ValueError as exc:
        _print_error(str(exc))

    if args.json:
        _print_json(cal.to_dict())
    else:
        print(_human(cal))


def cmd_version(_: argparse.Namespace) -> None:
    print(get_version())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mystilink-lunar",
        description="Mystilink Chinese lunar calendar CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert", help="Convert solar↔lunar and print year pillar")
    convert.add_argument("--date", help="Gregorian date YYYY-MM-DD")
    convert.add_argument("--lunar", help="Lunar date YYYY-MM-DD")
    convert.add_argument(
        "--leap",
        action="store_true",
        help="Treat --lunar as a leap month",
    )
    convert.add_argument("--time", help="Local time HH:MM or HH:MM:SS (default 00:00:00)")
    convert.add_argument(
        "--timezone",
        required=True,
        help="IANA timezone (required), e.g. Asia/Shanghai",
    )
    convert.add_argument(
        "--year-boundary",
        choices=["chunjie", "lichun_day", "lichun_exact"],
        default="chunjie",
        help="Year pillar / zodiac boundary (alpha.1: chunjie only)",
    )
    convert.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON",
    )
    convert.set_defaults(func=cmd_convert)

    ver = sub.add_parser("version", help="Print package version")
    ver.set_defaults(func=cmd_version)
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
