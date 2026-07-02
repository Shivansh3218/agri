# KrishiSetu — Deployment Guide

This repo IS the Frappe app **`drinkwell`** (KrishiSetu branding lives inside it).
App root = repo root, so it drops straight into `apps/drinkwell` on your server.

## 1. Push this code to GitHub (from your PC, in the `agri` folder)

```bash
cd agri
git init
git add .
git commit -m "KrishiSetu farmer platform"
git branch -M main
git remote add origin https://github.com/Shivansh3218/agri.git   # skip if already added
git push -u origin main --force
```
> Use a GitHub Personal Access Token as the password (Settings → Developer settings → Tokens, `repo` scope).

## 2. Put it on the server (replaces the current drinkwell app)

SSH into the server, then:

```bash
cd ~/frappe-bench/apps
mv drinkwell drinkwell_backup_$(date +%s)      # keep a backup of the old app
git clone https://github.com/Shivansh3218/agri.git drinkwell
```

## 3. Migrate, seed the data, build assets

```bash
cd ~/frappe-bench
bench --site production.local migrate
bench --site production.local execute drinkwell.api.seed.seed_data   # loads 396 farmers + crops + schemes
bench build --app drinkwell
bench --site production.local clear-cache
```

## 4. Make the KrishiSetu landing page the site home (once)

```bash
bench --site production.local set-config -g home_page "index"
# or in Desk: Website Settings → Home Page = index
```

## 5. Restart

```bash
sudo supervisorctl restart all
```

Open **http://13.233.98.60/** — you should see the KrishiSetu landing page.

## Pages
- `/` landing · `/dashboard` live analytics · `/survey` multi-step form
- `/farmers` directory · `/report?id=FARM0001` individual report
- `/insights` findings · `/schemes` govt schemes · `/about`

## Admin (Frappe Desk)
Log in at `/app`. New DocTypes appear under the **Drinkwell** module:
- Farmer Survey Response  → `/app/farmer-survey-response`
- Farmer                  → `/app/farmer`
- Crop                    → `/app/crop`
- Government Scheme        → `/app/government-scheme`

## Re-seeding
`seed_data` is idempotent — safe to run again; it skips records that already exist.

## Troubleshooting
- **No CSS on the website** → run `bench build --app drinkwell` and hard-refresh (Ctrl+Shift+R).
- **Dashboard/charts empty** → you skipped `seed_data`; run step 3 again.
- **404 on `/`** → set `home_page` (step 4) or check Website Settings → Home Page.
- **Migrate errors about old `survey` doctype** → harmless; the old app's tables stay in the DB but are unused.
