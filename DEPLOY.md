# Deploying to Render

## Repo layout

```
odoo-render-deploy/
├── Dockerfile
├── render.yaml
├── start.sh
├── repair.py
├── library/        <- copy of the library module
└── portfolio/      <- copy of the portfolio module
```

## Deploy

1. Render dashboard -> **New** -> **Blueprint** -> pick this repo -> **Deploy Blueprint**
2. Render creates a free PostgreSQL (`odoo-db`) and a Docker web service
   (`odoo-portfolio`). Later pushes to `main` redeploy automatically.

## First boot (automatic)

Render pre-creates an **empty** database. `start.sh` detects that and runs
Odoo with `-i base,library,portfolio --with-demo`, so there is no manual
"create database" step. Watch the service **Logs**: you should see
`start.sh: fresh database, initialising ...`, a long run of module loading,
and finally `admin password set from ADMIN_PASSWORD`.

On the free tier (0.1 CPU, 512 MB RAM) this first install is slow: expect
10-30 minutes. Keep opening the site every few minutes meanwhile, because a
free service with no incoming traffic spins down and interrupts the install.

Set `ODOO_DEMO=0` in the service's Environment to skip demo data.

## Logging in

- URL: the service's `onrender.com` address
- Login: `admin`
- Password: service -> **Environment** -> `ADMIN_PASSWORD` (reveal the value)

The public site is `/portfolio`.

## Free tier notes

- Cold starts: the first request after inactivity takes 30-50 s. After a
  restart the first page view is slower still, while Odoo rebuilds its CSS/JS.
- The free Postgres is deleted 30 days after creation.
- Sessions live on disk, so a restart logs everyone out.
- Upgrading: change `plan: free` to `starter` (web) / `basic-256mb` (db).

## Why the extra scripts exist

1. **Port collision.** The official image maps `HOST/PORT/USER/PASSWORD` to the
   DB connection, but Render reserves `PORT` for the port the app listens on.
   `start.sh` uses `DB_*` names and binds Odoo to `$PORT`.
2. **Empty database.** With exactly one empty database visible, Odoo picks it
   and answers every request with a 500 (`KeyError: 'ir.http'`). `start.sh`
   initialises it on first boot; the web database manager is switched off.
3. **Ephemeral disk.** The free tier wipes `/var/lib/odoo/filestore` on every
   spin-down, but the database still references those files, which produces
   `FileNotFoundError`, unstyled pages and 500s on `/web/image/...`.
   `repair.py` runs on every boot: it switches attachment storage to the
   database (`ir_attachment.location = db`) and drops records whose files
   are gone (CSS/JS bundles are regenerated on demand).
