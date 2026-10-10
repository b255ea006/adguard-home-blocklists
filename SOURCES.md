# Sources

This repository ships **curated starter lists**, not a mirror of large community feeds.
Entries are hand-picked for Homelab / AdGuard Home use and kept intentionally small.

## How entries get in

| Source type | How it is used |
|-------------|----------------|
| Manual curation | Domains observed in Homelab traffic or commonly known ad/tracker networks |
| Public knowledge | Well-known advertising, analytics, and adware networks |
| Companion feeds | Linked for users who need broader coverage; **not** imported wholesale |

## Companion lists (subscribe separately)

Prefer these as the heavy base layer; use this repo as a focused Homelab overlay:

- [AdGuard DNS filter](https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt)
- [AdGuard Tracking Protection](https://adguardteam.github.io/HostlistsRegistry/assets/filter_3.txt)
- [StevenBlack hosts (unified)](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) - convert or use a hosts-compatible pipeline
- Malware companion: [URLhaus hostfile](https://urlhaus.abuse.ch/downloads/hostfile/)

## File mapping

| File | Intent |
|------|--------|
| `lists/ads.txt` | Advertising / affiliate / ad-exchange hosts |
| `lists/tracking.txt` | Analytics, RUM, product telemetry |
| `lists/malware.txt` | Conservative adware / push / known-bad starters |
| `lists/all.txt` | Deduplicated union of the three (generated) |

## Regenerating `all.txt`

```bash
python scripts/build_all.py
python scripts/validate.py
```

## False positives

If a domain breaks banking, work SSO, smart-home cloud, or similar:

1. Whitelist it in AdGuard Home, and/or
2. Open an issue/PR with the domain and a short reason so it can be removed here.
