#!/usr/bin/env python3

import json
import subprocess
import datetime
from pathlib import Path

ITULIP_VERSION = "1.0-beta1"
AGENT_VERSION = "agent-1.0"

STATE_DIR = Path.home() / ".local/state/itulip"
REPORT_FILE = STATE_DIR / "report.json"


def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return "", str(e)


def block(status, summary, details=None):
    return {
        "status": status,
        "summary": summary,
        "details": details or {}
    }


def boot_info():
    out, _ = run(["systemd-analyze", "time"])
    if out:
        return block("ok", out)
    return block("unknown", "boot time unavailable")


def kernel_info():
    out, _ = run(["uname", "-r"])
    if out:
        return block("ok", f"Linux kernel {out}")
    return block("error", "kernel not detected")


def systemd_info():
    out, _ = run(["systemctl", "is-system-running"])
    if out == "running":
        return block("ok", "systemd running normally")
    if out:
        return block("warn", f"systemd state: {out}")
    return block("error", "systemd unreachable")


def graphics_info():
    out, _ = run(["loginctl", "show-session", "self", "-p", "Type"])
    if out:
        session = out.split("=")[-1]
        return block("ok", f"graphics session: {session}", {"session": session})
    return block("unknown", "graphics session unknown")


def user_session_info():
    out, _ = run(["systemctl", "--user", "is-system-running"])
    if out == "running":
        return block("ok", "user session running")
    if out:
        return block("warn", f"user session: {out}")
    return block("unknown", "user session state unknown")


def aggregate(blocks):
    priority = {"error": 3, "warn": 2, "ok": 1, "unknown": 0}
    worst = "unknown"
    for b in blocks.values():
        if priority[b["status"]] > priority[worst]:
            worst = b["status"]
    return worst


def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "itulip_version": ITULIP_VERSION,
        "agent_version": AGENT_VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",

        "boot": boot_info(),
        "kernel": kernel_info(),
        "systemd": systemd_info(),
        "graphics": graphics_info(),
        "user_session": user_session_info(),
    }

    report["system_status"] = aggregate({
        k: report[k]
        for k in ["boot", "kernel", "systemd", "graphics", "user_session"]
    })

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
