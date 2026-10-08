# Deploying to Render

## Repo layout

```
odoo-render-deploy/
├── Dockerfile
├── render.yaml
├── start.sh
├── library/        <- copy of the library module
└── portfolio/      <- copy of the portfolio module
```

## Deploy

1. Render dashboard -> **New** -> **Blueprint** -> pick this repo -> **Deploy Blueprint**
2. Render creates a free PostgreSQL (`odoo-db`) and a Docker web service
   (`odoo-portfolio`). Later pushes to `main` redeploy automatically.

## First boot (automatic)

Render pre-creates an **empty** database. `start.sh` detects that on boot and
runs Odoo with `-i base,library,portfolio --with-demo`, so there is no manual
"create database" step. Watch the service **Logs**: you should see
`start.sh: fresh database, initialising ...`, then a long run of module
loading, and finally `admin password set from ADMIN_PASSWORD`.

On the free tier (0.1 CPU, 512 MB RAM) this first install is slow — expect
10-30 minutes. Keep opening the site every few minutes meanwhile: a free
service with no incoming traffic spins down, which would interrupt the install.

Set `ODOO_DEMO=0` in the service's Environment to skip demo data.

## Logging in

- URL: the service's `onrender.com` address
- Login: `admin`
- Password: service -> **Environment** -> `ADMIN_PASSWORD` (reveal the value)

The public site is `/portfolio`.

## Free tier notes

- Cold starts: the first request after inactivity takes 30-50 s.
- The free Postgres is deleted 30 days after creation.
- No persistent disk: files uploaded through the Odoo UI reset on redeploy.
- Upgrading: change `plan: free` to `starter` (web) / `basic-256mb` (db).

## Why `start.sh` exists

1. The official image maps `HOST/PORT/USER/PASSWORD` to the DB connection, but
   Render reserves `PORT` for the port the app must listen on. The two collide
   and the deploy times out. `start.sh` uses `DB_*` names and binds Odoo to
   `$PORT` with `--http-port`.
2. With exactly one (empty) database visible, Odoo picks it automatically and
   answers every request with a 500 (`KeyError: 'ir.http'`). `start.sh`
   initialises that database on first boot instead of relying on the web
   database manager, which is also switched off (`--no-database-list`).
