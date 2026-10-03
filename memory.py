"""Customer memory for Barrios orders: "the regular".

Each customer (keyed by phone number) can save one regular order -
their usual. order_regular() replays it as a fresh order, so
"order the regular" works end to end.

Schema:
    customers(phone TEXT PK, name TEXT, regular_json TEXT,
              created_at TEXT, updated_at TEXT)

regular_json is a list of {item_id, name, quantity, unit_price_cents,
line_total_cents} - the same line shape orders.py persists.
"""

import json
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    phone TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    regular_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def save_regular(
    conn: sqlite3.Connection, name: str, phone: str, lines: list
) -> dict:
    """Save (or replace) a customer's regular order. lines is the
    validated line-item list. Returns the saved regular."""
    ensure_schema(conn)
    now = _now()
    conn.execute(
        "INSERT INTO customers (phone, name, regular_json, created_at,"
        " updated_at) VALUES (?, ?, ?, ?, ?)"
        " ON CONFLICT(phone) DO UPDATE SET name = excluded.name,"
        " regular_json = excluded.regular_json, updated_at = excluded.updated_at",
        (phone, name, json.dumps(lines), now, now),
    )
    conn.commit()
    return get_regular(conn, phone)


def get_regular(conn: sqlite3.Connection, phone: str):
    """Return a customer's saved regular, or None if they have none."""
    ensure_schema(conn)
    row = conn.execute(
        "SELECT * FROM customers WHERE phone = ?", (phone,)
    ).fetchone()
    if row is None:
        return None
    return {
        "customer_name": row["name"],
        "customer_phone": row["phone"],
        "regular": json.loads(row["regular_json"]),
        "updated_at": row["updated_at"],
    }
