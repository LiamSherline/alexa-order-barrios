"""SQLite persistence for Barrios orders.

Schema:
    orders(id TEXT PK, items_json TEXT, total_cents INTEGER,
           customer_name TEXT, customer_phone TEXT, status TEXT,
           created_at TEXT, updated_at TEXT)

Statuses: received -> preparing -> ready -> completed (or cancelled).
place_order always starts at "received". advance_status() is a demo helper
so the hackathon demo can walk an order through the kitchen flow.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    items_json TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

VALID_STATUSES = ("received", "preparing", "ready", "completed", "cancelled")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def _row_to_order(row: sqlite3.Row) -> dict:
    return {
        "order_id": row["id"],
        "items": json.loads(row["items_json"]),
        "total_cents": row["total_cents"],
        "total": f"${row['total_cents'] / 100:.2f}",
        "customer_name": row["customer_name"],
        "customer_phone": row["customer_phone"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def create_order(
    conn: sqlite3.Connection,
    items: list[dict],
    total_cents: int,
    customer_name: str,
    customer_phone: str,
) -> dict:
    """Persist a new order with status 'received'. items is a list of
    {item_id, name, quantity, unit_price_cents, line_total_cents}."""
    order_id = f"ord-{uuid.uuid4().hex[:8]}"
    now = _now()
    conn.execute(
        "INSERT INTO orders (id, items_json, total_cents, customer_name,"
        " customer_phone, status, created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            order_id,
            json.dumps(items),
            total_cents,
            customer_name,
            customer_phone,
            "received",
            now,
            now,
        ),
    )
    conn.commit()
    return get_order(conn, order_id)


def get_order(conn: sqlite3.Connection, order_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _row_to_order(row) if row else None


def advance_status(conn: sqlite3.Connection, order_id: str, status: str) -> dict:
    """Demo helper: move an order to a new status. Raises ValueError on
    unknown order or invalid status."""
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status {status!r}. Must be one of {VALID_STATUSES}."
        )
    order = get_order(conn, order_id)
    if order is None:
        raise ValueError(f"Unknown order id {order_id!r}.")
    conn.execute(
        "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
        (status, _now(), order_id),
    )
    conn.commit()
    return get_order(conn, order_id)
