# Alexa, order Barrios

MCP server for the Amazon Build, Ship, Shape hackathon (Alexa+ track):
"Alexa, order Barrios" lets a customer order pickup from Barrios Mexican
Cantina (Oak Ridge, TN) by voice. The Alexa+ skill calls these tools;
this repo is the self-hosted MCP server behind it.

## What it does

Three tools:

| Tool | What it does |
|---|---|
| `get_menu` | Full Barrios menu with prices (in cents) |
| `place_order` | Validates items against the menu, computes the total, persists the order with status `received` |
| `get_order_status` | Looks up an order by id: items, total, customer, status |

Menu data is the real menu from barriosoakridge.com (scraped 2026-10-02).
Prices are integers (cents). Locked facts: queso 4oz $3.50 / 8oz $7.00 /
16oz $13.00; guac 4oz $4.00 / 8oz $8.00 / 16oz $15.00.

## Run locally

```bash
cd ~/workspace/latch-hackathon/alexa-order-barrios
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# start the server (stdio transport, for MCP clients)
.venv/bin/python server.py
```

Orders persist to `./data/orders.db` (SQLite). Override with `BARRIOS_DB`:

```bash
BARRIOS_DB=/tmp/test.db .venv/bin/python server.py
```

## Test each tool

End-to-end through a real MCP client over stdio:

```bash
.venv/bin/python test_client.py
```

This asserts the acceptance case: 1x queso 8oz + 1x guac 4oz places an
order totaling $11.00 with status `received`, and `get_order_status`
returns it back.

With the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector .venv/bin/python server.py
```

Then call `get_menu`, `place_order`, `get_order_status` from the UI.

## Project layout

```
server.py            FastMCP server, the 3 tools
menu.py              menu data + lookup (source of truth: barriosoakridge.com)
orders.py            SQLite layer (orders table, advance_status demo helper)
adapters/aws_lambda.py  AWS boundary - NOT WIRED (see below)
test_client.py       stdio end-to-end test
requirements.txt     pinned
```

## AWS-later plan

AWS is not funded yet, so this repo is local-first: **no AWS SDK imports
anywhere** (`grep -rniE "boto3|botocore" --include="*.py" .` only matches
`adapters/` comments). When credits land:

1. **Hosting** - run the FastMCP server on Lambda (via Mangum) or
   ECS/Fargate; register its URL as the Alexa+ skill's MCP endpoint.
2. **Bedrock** - conversational layer (intent parsing, "the usual",
   recommendations) lives skill-side; Bedrock calls go in a new
   `adapters/bedrock_agent.py`, never in core.
3. **Persistence** - swap SQLite for DynamoDB/RDS via a new
   `adapters/dynamo_orders.py` implementing the same function signatures
   as `orders.py`, selected by `BARRIOS_ORDER_BACKEND`.
4. **Secrets** - Secrets Manager / Lambda env vars, never hardcoded.

See `adapters/aws_lambda.py` for the full boundary notes.
