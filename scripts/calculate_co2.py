#!/usr/bin/env python3
"""Calculate yesterday's accurate CO2 footprint.

Correlates Octopus Energy half-hourly consumption data with historical
half-hourly carbon intensity from the National Grid ESO Carbon Intensity
API, and stores the result in a Home Assistant input_number helper.

Usage:
    python3 scripts/calculate_co2.py

Requires: pip install websockets
"""

from __future__ import annotations

import asyncio
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    import websockets
except ImportError:
    print("ERROR: websockets package required. Install with: pip3 install websockets")
    sys.exit(1)

HA_URL = "ws://192.168.1.227:8123/api/websocket"
CARBON_API = "https://api.carbonintensity.org.uk/intensity/date"
HELPER_ENTITY = "input_number.yesterday_co2_grams"
HELPER_NAME = "Yesterday CO2 Grams"


def load_token() -> str:
    token_path = Path.home() / ".claude" / "accessToken"
    if not token_path.exists():
        print(f"ERROR: Token file not found at {token_path}")
        sys.exit(1)
    return token_path.read_text().strip()


def fetch_carbon_intensity(date_str: str) -> dict[str, float]:
    """Fetch half-hourly carbon intensity from the National Grid ESO API.

    Returns a dict mapping ISO start time -> actual intensity (gCO2/kWh).
    """
    url = f"{CARBON_API}/{date_str}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    intensity_map: dict[str, float] = {}
    for entry in data.get("data", []):
        start = entry["from"]
        # Prefer actual intensity, fall back to forecast
        actual = entry.get("intensity", {}).get("actual")
        forecast = entry.get("intensity", {}).get("forecast", 0)
        intensity_map[start] = actual if actual is not None else forecast

    return intensity_map


def normalise_timestamp(ts: str) -> str:
    """Normalise an ISO timestamp to YYYY-MM-DDTHH:MMZ for matching."""
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%dT%H:%MZ")


def calculate_co2(
    charges: list[dict], intensity_map: dict[str, float]
) -> tuple[float, int, int]:
    """Calculate total CO2 by correlating consumption with carbon intensity.

    Returns (total_co2_grams, matched_slots, total_slots).
    """
    # Normalise intensity map keys
    normalised = {normalise_timestamp(k): v for k, v in intensity_map.items()}

    total_co2 = 0.0
    matched = 0
    for charge in charges:
        key = normalise_timestamp(charge["start"])
        intensity = normalised.get(key)
        if intensity is not None:
            total_co2 += charge["consumption"] * intensity
            matched += 1

    return total_co2, matched, len(charges)


async def run(token: str) -> None:
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
        # Authenticate
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_resp = json.loads(await ws.recv())
        if auth_resp.get("type") != "auth_ok":
            print(f"ERROR: Authentication failed: {auth_resp}")
            sys.exit(1)
        print("Authenticated with Home Assistant")

        # Get all states to find the Octopus previous_cost sensor
        resp = await send(ws, {"type": "get_states"})
        if not resp.get("success"):
            print(f"ERROR: Failed to get states: {resp}")
            sys.exit(1)

        # Find the import previous_cost sensor (has charges attribute)
        charges = None
        sensor_id = None
        for state in resp["result"]:
            eid = state["entity_id"]
            if (
                "octopus_energy" in eid
                and "previous_cost" in eid
                and "export" not in eid
                and "gas" not in eid
            ):
                attrs = state.get("attributes", {})
                charges = attrs.get("charges", [])
                sensor_id = eid
                break

        if not charges:
            print("ERROR: No Octopus charges data found")
            sys.exit(1)

        print(f"Found {len(charges)} half-hourly slots from {sensor_id}")

        # Extract the date from the charges
        data_date = datetime.fromisoformat(charges[0]["start"]).strftime("%Y-%m-%d")
        print(f"Charges date: {data_date}")

        # Fetch carbon intensity for that date
        print(f"Fetching carbon intensity from {CARBON_API}/{data_date}")
        intensity_map = fetch_carbon_intensity(data_date)
        print(f"Got {len(intensity_map)} half-hourly intensity readings")

        # Calculate CO2
        total_co2, matched, total = calculate_co2(charges, intensity_map)
        print(
            f"Matched {matched}/{total} slots, "
            f"total CO2: {total_co2:.0f}g ({total_co2 / 1000:.2f}kg)"
        )

        if matched == 0:
            print("ERROR: No time slots matched between charges and intensity data")
            sys.exit(1)

        # Ensure the input_number helper exists
        resp = await send(ws, {"type": "get_states"})
        helper_exists = any(
            s["entity_id"] == HELPER_ENTITY for s in resp["result"]
        )

        if not helper_exists:
            print(f"Creating helper {HELPER_ENTITY}")
            resp = await send(
                ws,
                {
                    "type": "input_number/create",
                    "name": HELPER_NAME,
                    "min": 0,
                    "max": 1000000,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": "g",
                },
            )
            if not resp.get("success"):
                print(f"ERROR: Failed to create helper: {resp}")
                sys.exit(1)

        # Set the value
        resp = await send(
            ws,
            {
                "type": "call_service",
                "domain": "input_number",
                "service": "set_value",
                "service_data": {
                    "entity_id": HELPER_ENTITY,
                    "value": round(total_co2),
                },
            },
        )
        if not resp.get("success"):
            print(f"ERROR: Failed to set value: {resp}")
            sys.exit(1)

        print(
            f"Set {HELPER_ENTITY} = {total_co2:.0f}g "
            f"({total_co2 / 1000:.2f}kg) for {data_date}"
        )


def main() -> None:
    token = load_token()
    asyncio.run(run(token))


if __name__ == "__main__":
    main()
