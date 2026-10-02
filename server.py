"""Alexa, order Barrios - MCP server.

Exposes the restaurant ordering tools an Alexa+ skill calls:
    get_menu          full menu with prices
    place_order       validate items, compute total, persist order
    get_order_status  look up an order by id

Local-first: orders live in SQLite (BARRIOS_DB env var, default
./data/orders.db). No network calls, no AWS. When AWS hosting lands,
see adapters/aws_lambda.py - all cloud code stays behind that boundary.

Run:  .venv/bin/python server.py   (stdio transport for MCP clients)
"""

import os
import sys
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

import menu as menu_module
import orders as orders_db

mcp = FastMCP("barrios-order")

DB_PATH = os.environ.get(
    "BARRIOS_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "orders.db"),
)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _db():
    return orders_db.connect(DB_PATH)


@dataclass
class OrderLine:
    item_id: str
    quantity: int


@mcp.tool()
def get_menu() -> dict:
    """Return the full Barrios menu: categories, items, and prices in cents."""
    return menu_module.MENU


@mcp.tool()
def place_order(
    items: list, customer_name: str, customer_phone: str
) -> dict:
    """Place a pickup order.

    items: list of {"item_id": str, "quantity": int}. Every item_id is
    validated against the menu; unknown ids or non-positive quantities
    are rejected. Returns the persisted order with id, line items,
    total, and status "received".
    """
    if not items:
        return {"error": "Order must contain at least one item."}
    if not customer_name or not customer_name.strip():
        return {"error": "customer_name is required."}
    if not customer_phone or not customer_phone.strip():
        return {"error": "customer_phone is required."}

    lines: list[dict] = []
    total_cents = 0
    for raw in items:
        try:
            line = OrderLine(
                item_id=str(raw["item_id"]),
                quantity=int(raw["quantity"]),
            )
        except (KeyError, TypeError, ValueError):
            return {
                "error": f"Each item must be {{\"item_id\": str,"
                " \"quantity\": int}}."
            }
        if line.quantity <= 0:
            return {
                "error": f"Invalid quantity for {line.item_id!r}:"
                " must be a positive integer."
            }
        item = menu_module.get_item(line.item_id)
        if item is None:
            return {
                "error": f"Unknown menu item {line.item_id!r}."
                " Call get_menu for valid ids."
            }
        line_total = item["price_cents"] * line.quantity
        total_cents += line_total
        lines.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "quantity": line.quantity,
                "unit_price_cents": item["price_cents"],
                "line_total_cents": line_total,
            }
        )

    conn = _db()
    try:
        order = orders_db.create_order(
            conn, lines, total_cents, customer_name.strip(), customer_phone.strip()
        )
    finally:
        conn.close()
    return order


@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """Look up an order by id. Returns items, total, customer, and status."""
    conn = _db()
    try:
        order = orders_db.get_order(conn, order_id)
    finally:
        conn.close()
    if order is None:
        return {"error": f"Unknown order id {order_id!r}."}
    return order


if __name__ == "__main__":
    # FastMCP defaults to stdio transport, which is what MCP clients
    # (inspector, Alexa+ skill host) expect.
    mcp.run()
    sys.exit(0)
