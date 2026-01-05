#!/usr/bin/env python3

import json
import sys
from pathlib import Path

REPORT = Path.home() / ".local/state/itulip/report.json"

ICONS = {
    "ok": "🟢",
    "warn": "🟡",
    "error": "🔴",
    "unknown": "⚪"
}


def load():
    if not REPORT.exists():
        return None
    with open(REPORT) as f:
        return json.load(f)


def header(r):
    print(f"Itulip {r.get('itulip_version')} — Fedora system report\n")


def system_status(r):
    s = r.get("system_status", "unknown")
    print(f"SYSTEM STATUS: {ICONS[s]} {s.upper()}\n")


def block(name, b):
    icon = ICONS.get(b["status"], "⚪")
    title = name.replace("_", " ").title()
    print(f"{icon} {title}: {b['summary']}")


def main():
    r = load()
    if not r:
        print("Itulip: no data — agent not executed yet")
        sys.exit(1)

    header(r)
    system_status(r)

    for k in ["boot", "kernel", "systemd", "graphics", "user_session"]:
        block(k, r[k])


if __name__ == "__main__":
    main()
