"""AWS adapter boundary - NOT WIRED. Local-first until Liam funds AWS.

Everything cloud-specific lives in this file (and future siblings under
adapters/). Core modules (server.py, menu.py, orders.py) must NEVER import
boto3, botocore, or any AWS SDK. grep the repo to verify:

    grep -rniE "boto3|botocore|aws" --include="*.py" . | grep -v adapters/

Planned wiring (when AWS credits land):
  1. Hosting: run server.py's FastMCP app behind Mangum in AWS Lambda, or
     as a container on ECS/Fargate behind an ALB. The MCP server speaks
     stdio locally; for Lambda, wrap with Mangum (ASGI/HTTP) or keep the
     skill host calling a small HTTP shim that forwards to the tools.
     The Alexa+ skill registers this MCP server's URL as its tool endpoint.
  2. Bedrock: the Alexa+ skill's conversational layer (intent parsing,
     "the usual", dish recommendations) can call Bedrock models. That
     belongs in the SKILL-side agent config, not in this repo's core -
     keep Bedrock calls in adapters/bedrock_agent.py when the time comes.
  3. Persistence: swap SQLite for DynamoDB or RDS. orders.py exposes a
     small interface (connect/create_order/get_order/advance_status);
     add adapters/dynamo_orders.py implementing the same function
     signatures, and pick the backend via BARRIOS_ORDER_BACKEND env var.
  4. Secrets: DB creds / API keys via AWS Secrets Manager or Lambda env
     vars, never hardcoded.

Until then, this file is documentation. Do not import it.
"""

FUTURE = True
