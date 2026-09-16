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
from mystilink_lunar.solar_terms import get_solar_term

PACKAGE_NAME = "mystilink-lunar"
FALLBACK_VERSION = "0.1.0a3"


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


def _build_rules(args: argparse.Namespace) -> GanzhiRules:
    if getattr(args, "profile", None) == "bazi":
        base = GanzhiRules.bazi_default()
    else:
        base = GanzhiRules.lunar_calendar()
    return GanzhiRules(
        year_boundary=args.year_boundary or base.year_boundary,
        month_boundary=args.month_boundary or base.month_boundary,
        day_boundary=args.day_boundary or base.day_boundary,
        hour_system=base.hour_system,
    )


def _human(cal: LunarCalendar) -> str:
    lunar = cal.lunar
    leap = " leap" if lunar.is_leap_month else ""
    prev = cal.previous_solar_term
    nxt = cal.next_solar_term
    p = cal.pillars
    lines = [
        f"Solar       {cal.instant.isoformat()}",
        f"Timezone    {cal.timezone}",
        f"Lunar       {lunar.year}-{lunar.month:02d}-{lunar.day:02d}{leap}",
        f"Year        {p.year.text}",
        f"Month       {p.month.text}",
        f"Day         {p.day.text}",
        f"Hour        {p.hour.text}",
        f"Zodiac      {cal.zodiac.id} ({cal.zodiac.chinese})",
        f"Solar Term  {prev.chinese_name} → {nxt.chinese_name}",
        f"Rules       year={cal.rules.year_boundary} month={cal.rules.month_boundary} "
        f"day={cal.rules.day_boundary}",
        f"Provider    {cal.provider_name}",
    ]
    return "\n".join(lines)


def cmd_convert(args: argparse.Namespace) -> None:
    if not args.timezone:
        _print_error("timezone is required (IANA name, e.g. Asia/Shanghai)")
    try:
        hour, minute, second = _parse_time(args.time)
        rules = _build_rules(args)
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
        data = cal.to_dict()
        if args.explain:
            _pillars, trace = cal.ganzhi(explain=True)
            data["ganzhi_explain"] = trace.to_dict()
        _print_json(data)
    else:
        print(_human(cal))
        if args.explain:
            _pillars, trace = cal.ganzhi(explain=True)
            print("--- explain ---")
            for slot in ("year", "month", "day", "hour"):
                item = getattr(trace, slot)
                print(f"{slot:5} {item.value}  [{item.boundary}]  {item.reason}")


def cmd_solar_term(args: argparse.Namespace) -> None:
    try:
        term = get_solar_term(args.name, args.year, timezone=args.timezone)
    except MystilinkLunarError as exc:
        _print_error(str(exc))
    except ValueError as exc:
        _print_error(str(exc))

    if args.json:
        _print_json(term.to_dict())
        return
    print(
        f"{term.chinese_name} ({term.id})  {term.datetime.isoformat()}  "
        f"λ={term.solar_longitude:g}°"
    )


def cmd_version(_: argparse.Namespace) -> None:
    print(get_version())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mystilink-lunar",
        description="Mystilink Chinese lunar calendar CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert", help="Convert solar↔lunar and print four pillars")
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
        "--profile",
        choices=["lunar", "bazi"],
        default="lunar",
        help="Rule profile preset (default: lunar)",
    )
    convert.add_argument(
        "--year-boundary",
        choices=["chunjie", "lichun_day", "lichun_exact"],
        default=None,
        help="Override year pillar boundary",
    )
    convert.add_argument(
        "--month-boundary",
        choices=["jie_exact", "jie_day", "lunar_month"],
        default=None,
        help="Override month pillar boundary",
    )
    convert.add_argument(
        "--day-boundary",
        choices=["midnight", "zi_start"],
        default=None,
        help="Override day pillar boundary",
    )
    convert.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON",
    )
    convert.add_argument(
        "--explain",
        action="store_true",
        help="Include deterministic ganzhi rule traces",
    )
    convert.set_defaults(func=cmd_convert)

    term = sub.add_parser("solar-term", help="Exact instant of one 24 solar term")
    term.add_argument(
        "--name",
        required=True,
        help="Term id (lichun), Chinese name (立春), or index 0-23",
    )
    term.add_argument("--year", required=True, type=int, help="Gregorian year")
    term.add_argument(
        "--timezone",
        required=True,
        help="IANA timezone (required), e.g. Asia/Shanghai",
    )
    term.add_argument("--json", action="store_true", help="Print structured JSON")
    term.set_defaults(func=cmd_solar_term)

    ver = sub.add_parser("version", help="Print package version")
    ver.set_defaults(func=cmd_version)
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
