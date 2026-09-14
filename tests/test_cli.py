# -*- coding: utf-8 -*-
"""CLI smoke tests."""
from __future__ import annotations

import json
import subprocess
import sys


def test_cli_convert_json() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "mystilink_lunar",
            "convert",
            "--date",
            "1993-09-28",
            "--time",
            "13:21",
            "--timezone",
            "Asia/Shanghai",
            "--json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["lunar"]["month"] == 8
    assert data["lunar"]["day"] == 13
    assert data["ganzhi"]["year"]["text"] == "癸酉"


def test_cli_requires_timezone() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "mystilink_lunar",
            "convert",
            "--date",
            "1993-09-28",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
