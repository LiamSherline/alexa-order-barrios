"""Stdio test client for the Barrios MCP server.

Spawns server.py over stdio (same as the MCP inspector does) and exercises
all three tools end to end, including the $11.00 acceptance case:
1x queso 8oz ($7.00) + 1x guac 4oz ($4.00).

Usage:
    .venv/bin/python test_client.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(PROJECT_DIR, "server.py")
PYTHON = os.path.join(PROJECT_DIR, ".venv", "bin", "python")


def payload(res):
    """Extract the tool result payload: structured content when the SDK
    provides it, otherwise the JSON text block FastMCP always emits."""
    sc = getattr(res, "structuredContent", None)
    if sc:
        return sc.get("result", sc)
    return json.loads(res.content[0].text)


def check(name: str, cond: bool, detail: str = ""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" - {detail}" if detail else ""))
    if not cond:
        raise AssertionError(f"FAILED: {name} {detail}")


async def main() -> None:
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    env = dict(os.environ, BARRIOS_DB=tmp.name)

    params = StdioServerParameters(command=PYTHON, args=[SERVER], env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = sorted(t.name for t in tools.tools)
            print("tools:", tool_names)
            check(
                "six tools exposed",
                tool_names
                == [
                    "get_menu",
                    "get_order_status",
                    "get_recommendations",
                    "order_regular",
                    "place_order",
                    "save_regular",
                ],
                str(tool_names),
            )

            # 1. get_menu: locked prices present
            menu_res = await session.call_tool("get_menu", {})
            menu = payload(menu_res)
            items = {
                i["id"]: i
                for cat in menu["categories"]
                for i in cat["items"]
            }
            check("queso 4oz = $3.50", items["queso-4oz"]["price_cents"] == 350)
            check("queso 8oz = $7.00", items["queso-8oz"]["price_cents"] == 700)
            check("queso 16oz = $13.00", items["queso-16oz"]["price_cents"] == 1300)
            check("guac 4oz = $4.00", items["guac-4oz"]["price_cents"] == 400)
            check("guac 8oz = $8.00", items["guac-8oz"]["price_cents"] == 800)
            check("guac 16oz = $15.00", items["guac-16oz"]["price_cents"] == 1500)
            print(f"menu items total: {len(items)}")

            # 2. place_order: 1x queso 8oz + 1x guac 4oz = $11.00
            order_res = await session.call_tool(
                "place_order",
                {
                    "items": [
                        {"item_id": "queso-8oz", "quantity": 1},
                        {"item_id": "guac-4oz", "quantity": 1},
                    ],
                    "customer_name": "Test Customer",
                    "customer_phone": "8655550100",
                },
            )
            order = payload(order_res)
            check("no error on place_order", "error" not in order, str(order))
            check("total is $11.00", order["total_cents"] == 1100, order["total"])
            check("status starts received", order["status"] == "received")
            check("order_id present", order["order_id"].startswith("ord-"))
            order_id = order["order_id"]
            print(f"order_id: {order_id}")

            # 3. get_order_status returns the persisted order
            status_res = await session.call_tool(
                "get_order_status", {"order_id": order_id}
            )
            status = payload(status_res)
            check("status lookup finds order", status["order_id"] == order_id)
            check("status is received", status["status"] == "received")
            check("total persists", status["total_cents"] == 1100)

            # 4. unknown item rejected
            bad_res = await session.call_tool(
                "place_order",
                {
                    "items": [{"item_id": "not-a-taco", "quantity": 1}],
                    "customer_name": "X",
                    "customer_phone": "8655550100",
                },
            )
            bad = payload(bad_res)
            check("unknown item rejected", "error" in bad, str(bad))

            # 5. unknown order id
            missing_res = await session.call_tool(
                "get_order_status", {"order_id": "ord-nope"}
            )
            missing = payload(missing_res)
            check("unknown order rejected", "error" in missing, str(missing))

            # 6. save_regular: Liam's usual = 1x queso 8oz + 1x guac 4oz
            reg_res = await session.call_tool(
                "save_regular",
                {
                    "items": [
                        {"item_id": "queso-8oz", "quantity": 1},
                        {"item_id": "guac-4oz", "quantity": 1},
                    ],
                    "customer_name": "Liam",
                    "customer_phone": "8655550199",
                },
            )
            reg = payload(reg_res)
            check("no error on save_regular", "error" not in reg, str(reg))
            check(
                "regular total is $11.00",
                reg["total_cents"] == 1100,
                reg.get("total"),
            )
            check("regular has 2 lines", len(reg["regular"]) == 2)

            # 7. order_regular replays the saved regular as a new order
            reorder_res = await session.call_tool(
                "order_regular",
                {
                    "customer_name": "Liam",
                    "customer_phone": "8655550199",
                },
            )
            reorder = payload(reorder_res)
            check(
                "no error on order_regular", "error" not in reorder, str(reorder)
            )
            check(
                "regular order total $11.00",
                reorder["total_cents"] == 1100,
                reorder["total"],
            )
            check(
                "regular order starts received",
                reorder["status"] == "received",
            )
            check(
                "from_regular flagged",
                reorder.get("from_regular") is True,
            )
            check(
                "regular order is a new order",
                reorder["order_id"] != order_id,
                reorder["order_id"],
            )

            # 8. order_regular with no saved regular errors cleanly
            noreg_res = await session.call_tool(
                "order_regular",
                {
                    "customer_name": "Nobody",
                    "customer_phone": "8655550000",
                },
            )
            noreg = payload(noreg_res)
            check(
                "no regular -> clean error",
                "error" in noreg,
                str(noreg),
            )

            # 9. save_regular rejects unknown items like place_order
            badreg_res = await session.call_tool(
                "save_regular",
                {
                    "items": [{"item_id": "not-a-taco", "quantity": 1}],
                    "customer_name": "X",
                    "customer_phone": "8655550100",
                },
            )
            badreg = payload(badreg_res)
            check(
                "save_regular validates items",
                "error" in badreg,
                str(badreg),
            )

    # 6. advance_status demo helper (direct db layer)
    sys.path.insert(0, PROJECT_DIR)
    import orders as orders_db

    conn = orders_db.connect(tmp.name)
    moved = orders_db.advance_status(conn, order_id, "preparing")
    check("advance_status works", moved["status"] == "preparing")
    conn.close()

    os.unlink(tmp.name)
    print("\nAll checks passed.")


if __name__ == "__main__":
    asyncio.run(main())
