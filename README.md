# Itulip 🌱

Itulip is a Fedora-first system introspection tool designed to explain
*what actually happened* during system startup and user session initialization.

> Not a monitor. Not a logger.  
> A system explanation layer.

---

## Why Itulip?

Modern Linux systems are complex:
- firmware
- bootloader
- kernel
- initrd
- systemd
- user session
- graphics stack

Itulip connects these layers and presents them in a **human-readable way**.

---

## Architecture


- **Agent**: collects facts, never interprets
- **JSON**: stable data contract
- **CLI**: explains system state to humans

---

## Features (Beta 1)

- Boot time analysis
- Kernel detection
- systemd health state
- User session state
- Graphics session detection (basic)
- systemd --user integration

---

## Supported Platforms

- Fedora Linux (primary target)
- GNOME
- systemd
- Wayland / X11

Other distributions may work, but are not guaranteed.

---

## Installation (local)

```bash
cp agent/itulip_agent.py ~/.local/bin/itulip-agent
cp cli/itulip.py ~/.local/bin/itulip
chmod +x ~/.local/bin/itulip-agent ~/.local/bin/itulip

cp systemd/itulip-agent.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now itulip-agent.service


run itulip
