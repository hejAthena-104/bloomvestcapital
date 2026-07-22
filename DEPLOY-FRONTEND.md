# Frontend deployment — bloomvestcapital.com

**As of 2026-07-22 the marketing site is served from the Contabo VPS, not Netlify.**

| | |
|---|---|
| Live URL | https://bloomvestcapital.com (`www.` 301s to apex) |
| Served from | `/opt/bloomvest/repo/frontend` on `156.67.28.100` |
| Served by | the shared `swifteagle-caddy` container (`file_server`), mounted read-only at `/srv/bloomvest` |
| Dashboard | https://dashboard.bloomvestcapital.com — unchanged, still the `bloomvest-backend` Django container |

## Deploy a change

`frontend/` is tracked in git and served straight off disk — no build, no
container rebuild, no restart.

```bash
git add -A && git commit -m "frontend: ..." && git push

ssh -i ~/.ssh/id_ed25519 root@156.67.28.100 \
  'git -C /opt/bloomvest/repo pull --ff-only && chown -R 1000:1000 /opt/bloomvest'
```

Hard-reload the browser if you changed CSS/JS. That's the whole deploy.

> Backend changes are different — those still need
> `cd /opt/swifteagle && docker compose up -d --build bloomvest`.

## Routing (ported from `netlify.toml`)

| Path | Behaviour |
|---|---|
| `/` and `*.html` | static file from `frontend/` |
| `/about` (no extension) | resolves to `about.html` via `try_files` |
| `/login` | 302 → `dashboard.bloomvestcapital.com/auth/login/` |
| `/register` | 302 → `dashboard.bloomvestcapital.com/auth/register/` |
| `/auth/*` | 302 → dashboard host, path preserved |
| `/dashboard/*` | 302 → dashboard host, path preserved |

These rules now live in the `bloomvestcapital.com` block of
`/opt/swifteagle/Caddyfile`. `netlify.toml` is kept as the historical record and
the rollback path — it is no longer what serves the site.

## Rollback — ⚠️ Netlify is NOT currently a viable fallback

Checked at cutover (2026-07-22): all three Netlify origins return
**HTTP 503 `{"error":"usage_exceeded"}`** — the Netlify account has exceeded its
plan's usage limits, so the sites are hard-down there regardless of DNS. They
were already failing for real users *before* this migration.

Repointing DNS back to Netlify would therefore **restore an outage, not the
site**. To make that a real rollback path again you must first resolve the
Netlify account usage (wait for the monthly reset or upgrade the plan) and
confirm `https://<site>.netlify.app/` returns 200.

Practical rollback today = fix forward on the VPS (`git revert` + `git pull`),
which is fast because the frontend is served straight off disk.

If the Netlify account is healthy again, the DNS rollback is: apex A → `75.2.60.5`,
`www` CNAME → `bloomvestcapital-1.netlify.app`.

Full runbook, traps and the "add a new tenant" procedure:
`/opt/swifteagle/README.static-sites.md` on the VPS.
