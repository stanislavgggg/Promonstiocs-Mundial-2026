# email-rush — reworked for 2 Mundial 2026 football bots (per fifa2026-stack.md)

This repo already had the email engine + mini-app-opening bot. I configured it for the
2-bot football-tips setup. Rationale lives in `fifa2026-stack.md`; this is the repo-specific
summary.

## What changed
- **Added brand `futbolplus`** (concept = data/analysis, screenshot 1): ES-first, persona
  "Leo", Mundial 2026, compliant (no win-rate, 18+, no result guarantees).
- **Cleaned brand `goalcast`** (your 2nd football brand): removed the baked-in
  `win_rate_display=0.74` claim and rewrote the persona ES + Mundial + "sin garantías".
- **Bot opens the Mini App** via a persistent menu button too (from `MINI_APP_URL`), in
  addition to the existing inline button.

Run each bot as its own deploy: `BRAND_ID=futbolplus` and `BRAND_ID=goalcast`.

## Flow in this build = single opt-in (not double)
This repo's `capture.subscribe()` validates → checks consent → geo-gates → marks the
contact **confirmed** and **pushes to the ESP immediately**, tracking `esp_ok`. Failed
pushes are retried by `resync_esp.py` (run it on a Railway cron, e.g. every 15 min).
So: the email is owned in your Postgres AND pushed to the ESP on submit. SMTP is only
needed if you use the welcome mail — it's otherwise optional here.

## These are betting-tips → NOT Mailchimp
Football picks are gambling content; Mailchimp bans it. Set the football brands to the
hard segment and route to an iGaming-tolerant ESP:
```
EMAIL_HARD_VERTICALS=football,sports,betting,casino   # makes football "hard"
ESP_SOFT=noop
ESP_HARD=noop        # ← set to the iGaming ESP when chosen; until then emails are owned in PG
```

## Per-brand env (per Railway service)
```
BRAND_ID=futbolplus                      # or goalcast
DATABASE_URL=postgres://...              # REQUIRED (own list; bot+api are separate procs)
PUBLIC_API_BASE=https://<service>.up.railway.app
MINI_APP_URL=https://<lovable-page>      # the Mini App the bot opens (https only)
SITE_BASE=https://<lovable-page>
PRIVACY_URL=https://<lovable-page>/privacy
WRAPPER_TYPE=tips
CONSENT_VERSION=2026-06-v1

EMAIL_HARD_VERTICALS=football,sports,betting,casino
ESP_SOFT=noop
ESP_HARD=noop                            # iGaming ESP here

# optional welcome mail
SMTP_HOST=... SMTP_PORT=587 SMTP_USER=... SMTP_PASS=... EMAIL_FROM="fútbolplus <hi@...>"
```

## Notes
- **Geo-blocking removed.** There's no country gate in the code — targeting is handled
  entirely on your side (mini-app distribution, ad targeting, etc.).
- **These are betting-tips → NOT Mailchimp.** Football picks are gambling content;
  Mailchimp bans it. The football brands are the hard segment (`EMAIL_HARD_VERTICALS`)
  and route to `ESP_HARD` (an iGaming-tolerant ESP), never Mailchimp.
- **No win-rate claims** ("87%", "74%") — removed from goalcast; keep the mini-app copy on
  "análisis informativo".
- Mini-app copy/prompt: `fifa2026-miniapp-lovable-prompt.md`.

## Verified
Both brands load and capture end-to-end with `BRAND_ID=futbolplus` / `goalcast`:
MX (allow-list) → confirmed + routed to the hard-segment ESP; ES → geo-blocked. All
modules compile.

---

## Code review fixes (this pass)

- **Critical bug fixed:** both football brands crashed on startup — `conversation.py`
  (email-capture mode) needs `NUDGE / ALREADY_SUBSCRIBED / OPEN_APP_BTN`, which the old
  `copy_goalcast.py` didn't define. Rewrote `copy_goalcast.py` with those + the rest.
- **LATAM Spanish:** all user-facing ES copy was in Argentine **voseo** ("tocá", "dejá",
  "suscribite"…). Rewrote to **neutral LATAM (tuteo)** so it reads naturally in MX/CO/PE/CL/AR
  and ES alike. Removed Cherry-Rush leftovers (🍒 / "drop") from the shared success/error text.
- **Security:** `/api/erase` was unauthenticated (anyone could delete a contact by email).
  Now gated by `EMAIL_ADMIN_KEY` (header `X-Admin-Key`); if the env is unset the endpoint is
  disabled.
- **Hardening:** request bodies are capped at 256 KB (413 otherwise).
- Stale docstrings (single opt-in, multibrand) corrected.

## Retention pushes (new)

Leads who open the bot (`/start`) but don't leave their email get follow-up nudges with the
mini-app button, until they convert or block the bot.

- A **persistent** `email_leads` table (Postgres) tracks every bot opener — survives redeploys
  (unlike the JSON user store). `/start` upserts the lead; leaving an email (`tg_id` on
  subscribe, via fetch OR `WebApp.sendData`) marks it converted and stops the pushes.
- Run `python retention_push.py` on a **Railway cron** (e.g. hourly). It sends escalating
  copy (`REPEAT_PUSH`, 3 variants, LATAM ES) and marks users who blocked the bot so they're
  never pushed again.

Retention env (optional — sensible defaults):
```
RETENTION_MIN_AGE_H=24     # wait this long after /start before the first push
RETENTION_GAP_H=48         # min hours between pushes to one lead
RETENTION_MAX_PUSHES=3     # cap per lead
RETENTION_BATCH=200        # max sends per cron run
```

Other new env:
```
EMAIL_ADMIN_KEY=<secret>   # required to use POST /api/erase (header X-Admin-Key)
```
