# Home Assistant Energy Dashboards

Lovelace dashboard definitions and deploy scripts for a multi-integration Home Assistant energy monitoring setup.

## Dashboards

| Dashboard | File | Description |
|-----------|------|-------------|
| Octopus Energy | `dashboards/octopus-energy.yaml` | Agile tariff rates, consumption, costs |
| Energy Intelligence | `dashboards/energy-intelligence.yaml` | Cross-integration overview (Octopus + SolaX + Carbon) |
| Monthly Bills | `dashboards/energy-bills.yaml` | Monthly energy cost tracking and comparison |
| UK Carbon Intensity | `dashboards/uk-carbon-intensity.yaml` | Regional carbon intensity, forecasts, generation mix |
| Victron | `dashboards/victron.yaml` | Horsebox off-grid energy system |
| SolaX Energy | `dashboards/solax-energy.yaml` | Home solar, battery, and grid monitoring |

## Deploy Scripts

Each dashboard has a deploy script that:
1. Reads the HA token from `.claude/accessToken`
2. Connects to Home Assistant via WebSocket
3. Discovers entity IDs from the entity registry
4. Substitutes placeholders in the dashboard YAML template
5. Creates or updates the dashboard via the Lovelace API

```bash
# Install dependencies
pip3 install websockets pyyaml

# Deploy a specific dashboard
python3 scripts/deploy_octopus.py
python3 scripts/deploy_energy_intelligence.py
python3 scripts/deploy_energy_bills.py
python3 scripts/deploy_carbon_intensity.py
python3 scripts/deploy_victron.py
python3 scripts/deploy_solax.py
```

## Setup

Create a `.claude/accessToken` file in the repo root containing your Home Assistant long-lived access token.

## Documentation

- `docs/energy-metrics.md` — complete reference of available energy entities across all integrations
- `docs/outcome-focussed-dashboards.md` — architecture spec for outcome-driven dashboard design
