# AdGuard Home Blocklists

Curated DNS blocklists for [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome), in AdGuard filter format (`||domain^`).

Use them as **filter subscription** URLs so AdGuard Home refreshes them automatically.

## Quick start

In AdGuard Home:

1. **Filters** -> **DNS blocklists** -> **Add blocklist**
2. Choose **Add a custom list**
3. Paste one of the raw URLs below
4. Save and wait for the next filter update (or force update)

### Subscription URLs

| List | What it targets | Raw URL |
|------|-----------------|---------|
| **All (recommended)** | Ads + trackers + malware starters | `https://raw.githubusercontent.com/b255ea006/adguard-home-blocklists/main/lists/all.txt` |
| Ads | Common ad / affiliate hosts | `https://raw.githubusercontent.com/b255ea006/adguard-home-blocklists/main/lists/ads.txt` |
| Tracking | Analytics & telemetry hosts | `https://raw.githubusercontent.com/b255ea006/adguard-home-blocklists/main/lists/tracking.txt` |
| Malware | Known bad / phishing-style hosts (starter set) | `https://raw.githubusercontent.com/b255ea006/adguard-home-blocklists/main/lists/malware.txt` |

## Layout

```
lists/
  ads.txt
  tracking.txt
  malware.txt
  all.txt              # generated union of the three lists
scripts/
  build_all.py         # rebuild lists/all.txt
  validate.py          # syntax, duplicates, all.txt sync
.github/workflows/
  ci.yml               # runs build + validate on every push/PR
SOURCES.md             # curation notes and companion feeds
```

## Notes

- Lists are intentionally **small and maintained** - not a dump of every public blocklist.
- Prefer combining this with well-known community lists (see [SOURCES.md](SOURCES.md)) rather than replacing them.
- Always whitelist domains that break sites you need (banking, work SSO, smart home).
- Format: [AdGuard filter syntax](https://adguard.com/kb/general/ad-filtering/create-own-filters/)

## Develop

```bash
python scripts/build_all.py
python scripts/validate.py
```

CI fails if `lists/all.txt` is out of sync or a rule is invalid/duplicated.

## Contributing

Open an issue or PR with:

- domain to add/remove
- short reason (ad / tracker / malware / false positive)

## License

MIT - see [LICENSE](LICENSE).
