#!/usr/bin/env python3
"""Deploy the SolaX Energy dashboard to Home Assistant.

Connects via WebSocket, discovers solax_local entity IDs, substitutes
them into the dashboard template, and pushes via lovelace/dashboards/create
+ lovelace/config/save.

Usage:
    python3 scripts/deploy_solax.py

Requires: pip install websockets pyyaml
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

try:
    import websockets
except ImportError:
    print("ERROR: websockets package required. Install with: pip3 install websockets")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml package required. Install with: pip3 install pyyaml")
    sys.exit(1)

HA_URL = "ws://192.168.1.227:8123/api/websocket"
DASHBOARD_URL_PATH = "solax-energy"
DASHBOARD_TITLE = "SolaX Energy"
DASHBOARD_ICON = "mdi:solar-power"

PLACEHOLDER = "SOLAX_DEVICE"

# Known translation key suffixes — used to strip suffix and discover the prefix
KNOWN_SUFFIXES = [
    "grid_voltage",
    "grid_current",
    "grid_power",
    "grid_frequency",
    "grid_import_export",
    "pv1_voltage",
    "pv1_current",
    "pv1_power",
    "pv2_voltage",
    "pv2_current",
    "pv2_power",
    "battery_voltage",
    "battery_current",
    "battery_power",
    "battery_temperature",
    "battery_state_of_charge",
    "inverter_temperature",
    "total_pv_energy",
    "total_feed_in_energy",
    "total_consumption",
    "today_pv_energy",
]


def load_token() -> str:
    """Read the HA long-lived access token."""
    token_path = Path.home() / ".claude" / "accessToken"
    if not token_path.exists():
        print(f"ERROR: Token file not found at {token_path}")
        sys.exit(1)
    return token_path.read_text().strip()


def load_template() -> str:
    """Load the dashboard YAML template as a string."""
    template_path = (
        Path(__file__).resolve().parent.parent / "dashboards" / "solax-energy.yaml"
    )
    if not template_path.exists():
        print(f"ERROR: Dashboard template not found at {template_path}")
        sys.exit(1)
    return template_path.read_text()


def discover_prefix(entities: list[dict]) -> str:
    """Discover the entity prefix for solax_local sensors.

    Finds entities from platform 'solax_local', then strips a known suffix
    to determine the device prefix (e.g. 'solax_inverter_h4372ai4633110').
    """
    solax_entities = sorted(
        e["entity_id"]
        for e in entities
        if e.get("platform") == "solax_local"
        and e["entity_id"].startswith("sensor.")
    )

    if not solax_entities:
        print("ERROR: No solax_local sensor entities found in HA")
        sys.exit(1)

    print(f"Found {len(solax_entities)} solax_local sensor entities:")
    for eid in solax_entities:
        print(f"  {eid}")

    # Try to extract the prefix from any entity
    for eid in solax_entities:
        bare = eid[len("sensor."):]  # e.g. solax_inverter_h4372ai4633110_grid_voltage
        for suffix in KNOWN_SUFFIXES:
            if bare.endswith(f"_{suffix}"):
                prefix = bare[: -(len(suffix) + 1)]  # strip _suffix
                print(f"\nDiscovered device prefix: {prefix}")
                return prefix

    print("ERROR: Could not determine device prefix from entity IDs")
    sys.exit(1)


def substitute_template(template: str, prefix: str) -> dict:
    """Replace SOLAX_DEVICE placeholder with discovered prefix."""
    result = template.replace(PLACEHOLDER, prefix)

    # Warn about any remaining placeholders
    remaining = re.findall(r"SOLAX_DEVICE", result)
    if remaining:
        print(f"\nWARNING: {len(remaining)} unresolved SOLAX_DEVICE placeholder(s)")

    return yaml.safe_load(result)


async def deploy(token: str) -> None:
    """Connect to HA WebSocket and deploy the dashboard."""
    msg_id = 1

    async def send(ws, payload: dict) -> dict:
        nonlocal msg_id
        payload["id"] = msg_id
        msg_id += 1
        await ws.send(json.dumps(payload))
        while True:
            resp = json.loads(await ws.recv())
            if resp.get("id") == payload["id"]:
                return resp

    async with websockets.connect(HA_URL) as ws:
        # Wait for auth_required
        auth_req = json.loads(await ws.recv())
        if auth_req.get("type") != "auth_required":
            print(f"ERROR: Expected auth_required, got {auth_req.get('type')}")
            sys.exit(1)

        # Authenticate
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_resp = json.loads(await ws.recv())
        if auth_resp.get("type") != "auth_ok":
            print(f"ERROR: Authentication failed: {auth_resp}")
            sys.exit(1)
        print("Authenticated with Home Assistant\n")

        # Discover entities
        entity_resp = await send(ws, {"type": "config/entity_registry/list"})
        if not entity_resp.get("success"):
            print(f"ERROR: Failed to list entities: {entity_resp}")
            sys.exit(1)

        prefix = discover_prefix(entity_resp["result"])

        # Generate final config
        template = load_template()
        dashboard_config = substitute_template(template, prefix)

        # Check if dashboard already exists
        resp = await send(ws, {"type": "lovelace/dashboards/list"})
        if not resp.get("success"):
            print(f"ERROR: Failed to list dashboards: {resp}")
            sys.exit(1)

        existing = [
            d for d in resp["result"] if d.get("url_path") == DASHBOARD_URL_PATH
        ]

        if existing:
            print(
                f"\nDashboard '{DASHBOARD_URL_PATH}' already exists, updating config..."
            )
        else:
            create_resp = await send(
                ws,
                {
                    "type": "lovelace/dashboards/create",
                    "url_path": DASHBOARD_URL_PATH,
                    "title": DASHBOARD_TITLE,
                    "icon": DASHBOARD_ICON,
                    "require_admin": False,
                    "show_in_sidebar": True,
                },
            )
            if not create_resp.get("success"):
                print(f"ERROR: Failed to create dashboard: {create_resp}")
                sys.exit(1)
            print(f"\nCreated dashboard at /{DASHBOARD_URL_PATH}")

        # Save the dashboard config
        save_resp = await send(
            ws,
            {
                "type": "lovelace/config/save",
                "url_path": DASHBOARD_URL_PATH,
                "config": dashboard_config,
            },
        )
        if not save_resp.get("success"):
            print(f"ERROR: Failed to save dashboard config: {save_resp}")
            sys.exit(1)

        print("Dashboard config saved successfully!")
        print(f"View at: http://192.168.1.227:8123/{DASHBOARD_URL_PATH}")


def main() -> None:
    token = load_token()
    asyncio.run(deploy(token))


if __name__ == "__main__":
    main()
