# Deploying to Render

## 1. Assemble the deploy repo

Create a new GitHub repo (e.g. `odoo-render-deploy`), and inside it:

```
odoo-render-deploy/
├── Dockerfile
├── render.yaml
├── library/        <- copy of your library module's files
└── portfolio/      <- copy of your portfolio module's files
```

Just copy the module folders directly (don't use git submodules here —
keeps the Render build simple and avoids submodule edge cases).

## 2. Create the Blueprint on Render

1. Go to https://dashboard.render.com → **New** → **Blueprint**
2. Connect your GitHub account and select the new repo
3. Render reads `render.yaml` and proposes: one **Web Service**
   (`odoo-portfolio`, Docker) + one **PostgreSQL** database (`odoo-db`)
4. Click **Apply** — first build takes a few minutes (Render builds the
   Docker image, pulls `odoo:19`, copies in the addons)

## 3. First-time setup (one-off, via the browser)

Once it's live at `https://odoo-portfolio-xxxx.onrender.com`:

1. You'll land on the **Database Manager** screen (no database exists yet)
2. Create a database (pick any name, e.g. `prod`), set an admin email/password
   — this becomes your Odoo login, not the server's
3. **Important**: the *master password* for the Database Manager itself
   defaults to `admin` in the base image. Change it immediately after first
   login: Settings → General Settings → bottom of page, or via
   `--master-password` — otherwise anyone can see/delete your database from
   that screen. Ask me if you want a hardened config for this.
4. Go to **Apps**, remove the "Apps" filter, search `library` → Install.
   Do the same for `portfolio`.
5. Visit `/portfolio` on your Render URL — your page should be live.

## 4. Notes (free tier)

- **Cold starts**: the free web service spins down after a period of
  inactivity. The first request afterward can take 30-50 seconds while it
  wakes up — normal, not a bug.
- **Database expiry**: Render's free Postgres instance is **deleted 30 days
  after creation**. Put a reminder in your calendar — you'll need to spin up
  a fresh `odoo-db`, reconnect it, and reinstall `library`/`portfolio` when
  that happens (or upgrade to a paid Postgres plan before then to keep it).
- **No persistent disk**: free web services can't attach a disk, so Odoo's
  filestore (uploaded attachments/images added *through the UI*, not the
  ones baked into the Docker image) resets on every redeploy. Fine for a
  demo; move to a paid web plan + disk later if that becomes an issue.
- **Updating modules later**: pushing to the connected branch triggers a
  Render rebuild automatically, but installed-app code changes still need
  an explicit module update (Apps → your module → Upgrade) to take effect
  in the running database.
- **Upgrading later**: when you want reliability (e.g. before a key
  interview), just change `plan: free` to `plan: starter` (web) and
  `plan: basic-256mb` (database) in `render.yaml`, push, and add a persistent
  disk back for the web service.
