"""AWS Bedrock integration for Alexa, order Barrios.

Provides AI-powered dish recommendations using Amazon Bedrock.
This is the AWS Builder mini-challenge integration: the MCP server
calls Bedrock at runtime to generate personalized menu suggestions.

All boto3/botocore imports live in this file (and adapters/ only).
Core modules never import AWS SDKs.

Setup:
    pip install boto3
    export AWS_REGION=us-east-2  (or your region)
    # Credentials via standard AWS chain (env vars, ~/.aws/credentials, IAM role)

Model: anthropic.claude-3-haiku-20240307-v1:0 (cheap, fast, good enough
for recommendations). Override with BARRIOS_BEDROCK_MODEL.
"""

from __future__ import annotations

import json
import os

import menu as menu_module

MODEL_ID = os.environ.get(
    "BARRIOS_BEDROCK_MODEL",
    "anthropic.claude-3-haiku-20240307-v1:0",
)
REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-2"))
MAX_TOKENS = 500


def _menu_summary() -> str:
    """Flatten the menu into a compact text list for the prompt."""
    lines = []
    for cat in menu_module.MENU["categories"]:
        for item in cat["items"]:
            price = item["price_cents"] / 100
            lines.append(f"- {item['id']}: {item['name']} (${price:.2f}) [{cat['name']}]")
    return "\n".join(lines)


def _bedrock_client():
    import boto3

    return boto3.client("bedrock-runtime", region_name=REGION)


def get_recommendations(preference: str, count: int = 3) -> dict:
    """Ask Bedrock for dish recommendations matching a preference.

    Args:
        preference: free text like "spicy", "vegetarian", "something light",
            "feeding a group of 4".
        count: how many dishes to suggest (1-5).

    Returns:
        {"recommendations": [{"item_id": ..., "name": ..., "price_cents": ...,
                              "reason": ...}, ...]}
        or {"error": ...} if Bedrock is unreachable.
    """
    count = max(1, min(count, 5))
    menu_text = _menu_summary()

    prompt = (
        "You are a helpful restaurant assistant for Barrios Mexican Cantina. "
        f"A customer says: {preference!r}\n\n"
        f"Recommend exactly {count} dishes from this menu. "
        "For each, give the item_id, a one-sentence reason tied to their preference.\n\n"
        f"MENU:\n{menu_text}\n\n"
        'Respond ONLY with valid JSON: {"recommendations": '
        '[{"item_id": "...", "reason": "..."}]}'
    )

    try:
        client = _bedrock_client()
        resp = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": MAX_TOKENS,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ),
        )
        body = json.loads(resp["body"].read())
        text = body["content"][0]["text"]
        # Strip markdown fences if the model adds them
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        parsed = json.loads(text)
    except Exception as e:  # boto3, network, model, JSON parse
        return {"error": f"Bedrock unavailable: {e}"}

    # Enrich with real menu data (name, price) so callers can order directly
    by_id = {}
    for cat in menu_module.MENU["categories"]:
        for item in cat["items"]:
            by_id[item["id"]] = item

    out = []
    for rec in parsed.get("recommendations", [])[:count]:
        item = by_id.get(rec.get("item_id"))
        if not item:
            continue
        out.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "price_cents": item["price_cents"],
                "reason": rec.get("reason", ""),
            }
        )
    return {"recommendations": out}
