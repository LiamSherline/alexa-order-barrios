"""Alexa, order Barrios - MCP server.

Exposes the restaurant ordering tools an Alexa+ skill calls:
    get_menu          full menu with prices
    place_order       validate items, compute total, persist order
    get_order_status  look up an order by id
    save_regular      remember a customer's usual ("my regular")
    order_regular     replay the saved regular as a new order

Local-first: orders and customer memory live in SQLite (BARRIOS_DB env
var, default ./data/orders.db). No network calls, no AWS. When AWS
hosting lands, see adapters/aws_lambda.py - all cloud code stays behind
that boundary.

Run:  .venv/bin/python server.py   (stdio transport for MCP clients)
"""

import os
import sys

from mcp.server.fastmcp import FastMCP

import menu as menu_module
import orders as orders_db
import memory as memory_db

mcp = FastMCP("barrios-order")

DB_PATH = os.environ.get(
    "BARRIOS_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "orders.db"),
)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _db():
    return orders_db.connect(DB_PATH)


@mcp.tool()
def get_menu() -> dict:
    """Return the full Barrios menu: categories, items, and prices in cents."""
    return menu_module.MENU


def _validate_lines(items):
    """Validate raw item dicts against the menu. Returns
    (lines, total_cents) or (None, error_dict)."""
    lines = []
    total_cents = 0
    for raw in items:
        try:
            item_id = str(raw["item_id"])
            quantity = int(raw["quantity"])
        except (KeyError, TypeError, ValueError):
            return None, {
                "error": 'Each item must be {"item_id": str,'
                ' "quantity": int}.'
            }
        if quantity <= 0:
            return None, {
                "error": f"Invalid quantity for {item_id!r}:"
                " must be a positive integer."
            }
        item = menu_module.get_item(item_id)
        if item is None:
            return None, {
                "error": f"Unknown menu item {item_id!r}."
                " Call get_menu for valid ids."
            }
        line_total = item["price_cents"] * quantity
        total_cents += line_total
        lines.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "quantity": quantity,
                "unit_price_cents": item["price_cents"],
                "line_total_cents": line_total,
            }
        )
    return lines, total_cents


def _persist_order(lines, total_cents, customer_name, customer_phone):
    conn = _db()
    try:
        order = orders_db.create_order(
            conn, lines, total_cents, customer_name, customer_phone
        )
    finally:
        conn.close()
    return order


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

    lines, total = _validate_lines(items)
    if lines is None:
        return total  # error dict
    return _persist_order(
        lines, total, customer_name.strip(), customer_phone.strip()
    )


@mcp.tool()
def save_regular(
    items: list, customer_name: str, customer_phone: str
) -> dict:
    """Remember a customer's regular order ("my usual").

    items: list of {"item_id": str, "quantity": int}, validated against
    the menu exactly like place_order. Replaces any previously saved
    regular for this phone number. Returns the saved regular.
    """
    if not items:
        return {"error": "Regular must contain at least one item."}
    if not customer_name or not customer_name.strip():
        return {"error": "customer_name is required."}
    if not customer_phone or not customer_phone.strip():
        return {"error": "customer_phone is required."}

    lines, total = _validate_lines(items)
    if lines is None:
        return total  # error dict

    conn = _db()
    try:
        regular = memory_db.save_regular(
            conn, customer_name.strip(), customer_phone.strip(), lines
        )
    finally:
        conn.close()
    regular["total_cents"] = total
    regular["total"] = f"${total / 100:.2f}"
    return regular


@mcp.tool()
def order_regular(customer_name: str, customer_phone: str) -> dict:
    """Place a pickup order from the customer's saved regular
    ("order the regular"). Replays their usual items as a brand-new
    order with status "received". Errors if no regular is saved.
    """
    if not customer_name or not customer_name.strip():
        return {"error": "customer_name is required."}
    if not customer_phone or not customer_phone.strip():
        return {"error": "customer_phone is required."}

    conn = _db()
    try:
        regular = memory_db.get_regular(conn, customer_phone.strip())
    finally:
        conn.close()
    if regular is None:
        return {
            "error": "No regular saved for this customer."
            " Call save_regular first."
        }

    lines = regular["regular"]
    total_cents = sum(
        line["line_total_cents"] for line in lines
    )
    order = _persist_order(
        lines, total_cents, customer_name.strip(), customer_phone.strip()
    )
    order["from_regular"] = True
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
    # Transport selectable via BARRIOS_TRANSPORT env var:
    #   stdio (default) - for MCP clients (inspector, local testing)
    #   streamable-http - for remote hosting (Alexa+ skill host, demos)
    #   sse             - legacy SSE, kept for compatibility
    # For streamable-http, set BARRIOS_PORT (default 8000).
    transport = os.environ.get("BARRIOS_TRANSPORT", "stdio")
    if transport == "streamable-http":
        import uvicorn

        port = int(os.environ.get("BARRIOS_PORT", "8000"))
        app = mcp.streamable_http_app()
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run(transport=transport)
    sys.exit(0)
