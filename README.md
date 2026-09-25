# Linux Security Audit Script

A Python automation tool that generates a quick security/system audit report for a Linux machine using `subprocess`.

## What it does

Runs a series of system commands and prints a clean, formatted report covering:

- **System Info** — CPU model, RAM usage, disk usage
- **Disk Partitions** — block devices and mount points (via `lsblk -J`)
- **User Accounts** — usernames, home directories, shells (from `/etc/passwd`)
- **Network Info** — IPv4/IPv6 addresses, default gateway, DNS servers
- **Listening Ports** — active TCP/UDP listeners (via `ss -tuln`)
- **Security Logs** — counts of failed logins, auth failures, permission denials, sudo/ssh activity, errors, and warnings (via `journalctl`)

## Requirements

- Linux OS
- Python 3
- Standard system tools: `lscpu`, `free`, `df`, `lsblk`, `ip`, `ss`, `journalctl`

## Usage

```bash
python3 security_report.py
```

No arguments needed — it runs the full audit and prints the report to stdout.

## Example Output

```
============================================================
                 LINUX SECURITY AUDIT
============================================================

────────────────────────────────────────────────────────────
                    SYSTEM INFORMATION
────────────────────────────────────────────────────────────
CPU MODEL: Intel(R) Core(TM) i5-...
Total RAM: 7.6G
Used RAM: 3.2G
Free RAM: 1.1G
```


## Notes

This is an early-stage learning project focused on Python automation with `subprocess` and `json`. Planned improvements:

- CLI flags (e.g. `--section network`, `--json`, `--output report.txt`)
- Error handling for missing commands/permissions
- Exporting results to JSON/HTML
- Severity scoring for log findings

## Disclaimer

For educational/personal use on systems you own or are authorized to audit.
