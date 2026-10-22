#!/bin/sh
set -e

: "${DB_NAME:?DB_NAME is not set}"

DB_ARGS="--db_host=$DB_HOST --db_port=$DB_PORT --db_user=$DB_USER --db_password=$DB_PASSWORD"

# The free tier's disk is wiped on every restart; see repair.py. Exit code 10
# means "new deploy: upgrade the installed modules" (-u), anything else
# non-zero is ignored.
UPDATE_ARGS=""
if python3 /repair.py; then
    :
else
    rc=$?
    if [ "$rc" = "10" ]; then
        UPDATE_ARGS="-u library,portfolio"
        echo "start.sh: new deploy detected, upgrading library + portfolio"
    else
        echo "start.sh: repair step failed with code $rc (ignored)"
    fi
fi

# Is the Render-provided database already initialised with our modules?
if python3 - <<'PY'
import os, sys
import psycopg2
try:
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"],
    )
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('public.ir_module_module')")
    if cur.fetchone()[0] is None:
        sys.exit(1)
    cur.execute("SELECT 1 FROM ir_module_module WHERE name = 'portfolio' AND state = 'installed'")
    sys.exit(0 if cur.fetchone() else 1)
except Exception as exc:
    print("db check failed:", exc, file=sys.stderr)
    sys.exit(1)
PY
then
    INIT_ARGS=""
    echo "start.sh: database already initialised, starting normally"
else
    INIT_ARGS="-i base,library,portfolio"
    if [ "${ODOO_DEMO:-1}" = "1" ]; then
        INIT_ARGS="$INIT_ARGS --with-demo"
    fi
    echo "start.sh: fresh database, initialising with: $INIT_ARGS"

    # Background helper: once the modules are installed, set the admin
    # password from $ADMIN_PASSWORD (first boot only, so a password you
    # change later is never overwritten by a redeploy).
    if [ -n "$ADMIN_PASSWORD" ]; then
        (
            python3 - <<'PY'
import os, time
import psycopg2
from passlib.context import CryptContext

ctx = CryptContext(schemes=["pbkdf2_sha512"])
params = dict(
    host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
    user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"],
    dbname=os.environ["DB_NAME"],
)
for _ in range(240):  # up to ~60 minutes
    time.sleep(15)
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.ir_module_module')")
        if cur.fetchone()[0] is None:
            conn.close()
            continue
        cur.execute("SELECT 1 FROM ir_module_module WHERE name = 'portfolio' AND state = 'installed'")
        if not cur.fetchone():
            conn.close()
            continue
        cur.execute("UPDATE res_users SET password = %s WHERE login = 'admin'",
                    (ctx.hash(os.environ["ADMIN_PASSWORD"]),))
        conn.commit()
        conn.close()
        print("start.sh: admin password set from ADMIN_PASSWORD", flush=True)
        break
    except Exception as exc:
        print("start.sh: admin password helper retrying:", exc, flush=True)
PY
        ) &
    fi
fi

python3 - <<'PY' || true
import os
import psycopg2
from passlib.context import CryptContext

ctx = CryptContext(schemes=["pbkdf2_sha512"])
DEMO_IDS = "SELECT res_id FROM ir_model_data WHERE module = 'library' AND model = %s"
try:
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"],
    )
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('public.res_users'), to_regclass('public.library_loan')")
    users_table, loan_table = cur.fetchone()
    has_demo_users = False
    if users_table is not None:
        cur.execute("SELECT 1 FROM res_users WHERE login = 'librarian'")
        has_demo_users = cur.fetchone() is not None
    if has_demo_users:
        for login in ("librarian", "member"):
            cur.execute("UPDATE res_users SET password = %s WHERE login = %s",
                        (ctx.hash(login), login))
        conn.commit()
        print("start.sh: demo user passwords reset", flush=True)
    if has_demo_users and loan_table is not None:
        cur.execute("DELETE FROM library_loan WHERE id NOT IN (" + DEMO_IDS + ")",
                    ("library.loan",))
        cur.execute(
            "UPDATE res_partner SET active = false WHERE id IN ("
            "SELECT partner_id FROM library_member WHERE id NOT IN (" + DEMO_IDS + "))",
            ("library.member",),
        )
        cur.execute("DELETE FROM library_member WHERE id NOT IN (" + DEMO_IDS + ")",
                    ("library.member",))
        cur.execute("DELETE FROM library_book WHERE id NOT IN (" + DEMO_IDS + ")",
                    ("library.book",))
        cur.execute(
            "UPDATE library_loan SET state = 'ongoing', return_date = NULL WHERE id IN ("
            "SELECT res_id FROM ir_model_data WHERE module = 'library' "
            "AND model = 'library.loan' "
            "AND name IN ('demo_loan_ongoing', 'demo_loan_overdue', 'demo_loan_marie_ongoing'))"
        )
        cur.execute(
            "UPDATE library_book b SET is_available = NOT EXISTS ("
            "SELECT 1 FROM library_loan l WHERE l.book_id = b.id AND l.state = 'ongoing')"
        )
        conn.commit()
        print("start.sh: visitor data cleaned up", flush=True)
    conn.close()
except Exception as exc:
    print("start.sh: demo cleanup skipped:", exc, flush=True)
PY

exec odoo $DB_ARGS -d "$DB_NAME" --db-filter="^${DB_NAME}\$" --no-database-list --http-port="$PORT" $INIT_ARGS $UPDATE_ARGS
