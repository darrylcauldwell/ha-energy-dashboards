# Available Energy Metrics

---

### SolaX (Home Solar + Battery)

#### Real-time Power (state_class: measurement, live W)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.solax_pv_power_total` | Total solar generation | 0 W (night) |
| `sensor.solax_pv_power_1` | PV string 1 power | 0 W |
| `sensor.solax_pv_power_2` | PV string 2 power | 0 W |
| `sensor.solax_pv_voltage_1` | PV string 1 voltage | 0 V |
| `sensor.solax_pv_voltage_2` | PV string 2 voltage | 0 V |
| `sensor.solax_house_load` | Total house consumption | 640 W |
| `sensor.solax_battery_power_charge` | Battery power (negative=charging, positive=discharging) | -678 W |
| `sensor.solax_grid_import` | Power drawn from grid | 0 W |
| `sensor.solax_grid_export` | Power exported to grid | 0 W |
| `sensor.solax_inverter_power` | Inverter output power | 640 W |
| `sensor.solax_inverter_voltage` | Inverter AC voltage | 245.3 V |
| `sensor.solax_inverter_frequency` | AC frequency | 50.11 Hz |
| `sensor.solax_inverter_current` | Inverter current | 2.7 A |
| `sensor.solax_battery_capacity` | Battery SOC % | 68% |
| `sensor.solax_battery_voltage_charge` | Battery voltage | 230 V |
| `sensor.solax_battery_current_charge` | Battery current | -3.0 A |
| `sensor.solax_battery_temperature` | Battery temperature | 20°C |
| `sensor.solax_inverter_temperature` | Inverter temperature | 32°C |

#### Today's Energy Totals (state_class: total_increasing, resets midnight)

| Entity | Description | Today |
|--------|-------------|-------|
| `sensor.solax_today_s_solar_energy` | Solar energy produced today | 9.8 kWh |
| `sensor.solax_today_s_import_energy` | Grid energy imported today | 12.5 kWh |
| `sensor.solax_today_s_export_energy` | Grid energy exported today | 5.4 kWh |
| `sensor.solax_today_s_yield` | Total inverter yield today | 11.9 kWh |
| `sensor.solax_battery_input_energy_today` | Energy charged into battery today | 6.6 kWh |
| `sensor.solax_battery_output_energy_today` | Energy discharged from battery today | 3.3 kWh |

#### Lifetime Totals (state_class: total_increasing)

| Entity | Description | Total |
|--------|-------------|-------|
| `sensor.solax_total_solar_energy` | All-time solar production | 8,437 kWh |
| `sensor.solax_total_yield` | All-time inverter yield | 11,281 kWh |
| `sensor.solax_energy_from_grid` | All-time grid import | 7,448 kWh |
| `sensor.solax_energy_to_grid` | All-time grid export | 2,952 kWh |

#### Operating Mode & Schedule

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.solax_run_mode` | Inverter run mode | Normal Mode |
| `select.solax_charger_use_mode` | Charge strategy | Self Use Mode |
| `select.solax_charger_start_time_1` | Charge window 1 start | 01:00 |
| `select.solax_charger_end_time_1` | Charge window 1 end | 05:00 |
| `select.solax_charger_start_time_2` | Charge window 2 start | 14:30 |
| `select.solax_charger_end_time_2` | Charge window 2 end | 15:30 |
| `select.solax_discharger_start_time_1` | Discharge window 1 start | 12:00 |
| `select.solax_discharger_end_time_1` | Discharge window 1 end | 23:59 |
| `select.solax_selfuse_night_charge_enable` | Night charging enabled | Enabled |
| `number.solax_selfuse_nightcharge_upper_soc` | Night charge ceiling SOC | 90% |
| `number.solax_selfuse_discharge_min_soc` | Minimum discharge SOC | 10% |
| `select.solax_manual_mode_control` | Manual override | Off |

#### SolaX EV Charger

All EV charger entities report `unknown` when no vehicle is connected. The SolaX Modbus integration exposes **controls only** — there are no sensor entities for live charging power, session energy, or charger status. Energy consumed during a charge session can only be inferred from the increase in `solax_today_s_import_energy` or `solax_house_load` while charging.

Three entities are disabled by the integration by default and would need enabling in the HA entity registry if required:

| Entity | Description | State |
|--------|-------------|-------|
| `number.solax_ev_charger_charge_current` | Charge current setpoint | 6–32 A (unknown when no EV) |
| `select.solax_ev_charger_charger_use_mode` | Charge mode | Stop / Fast / ECO / Green |
| `select.solax_ev_charger_boost_mode` | Boost mode | Normal / Timer Boost / Smart Boost |
| `select.solax_ev_charger_control_command` | Manual command | Available / Start Charging / Stop Charging / Reserve |
| `select.solax_ev_charger_eco_gear` | ECO mode max current | 6A / 10A / 16A / 20A / 25A |
| `select.solax_ev_charger_green_gear` | Green mode max current (solar-only) | 3A / 6A |
| `select.solax_ev_charger_device_lock` | Lock/unlock charger | Lock / Unlock |
| `select.solax_ev_charger_rfid_program` | RFID card programming | — |
| `button.solax_ev_charger_sync_rtc` | Sync charger clock | — |
| `number.solax_ev_charger_address` *(disabled)* | Modbus address | — |
| `select.solax_battery_to_ev_charger` *(disabled)* | Allow battery to charge EV | — |
| `select.solax_ev_charger_meter_setting` *(disabled)* | Meter configuration | — |

**Mode guide:**
- **Fast**: Charges at full `charge_current` setpoint regardless of solar
- **ECO**: Charges at a minimum baseline (ECO gear current) plus any surplus solar, up to the setpoint
- **Green**: Charges only from solar surplus, at Green gear current (3A or 6A minimum threshold)

**Gap**: No native sensor for session kWh, charging state, or connected vehicle. To measure EV charging energy precisely, a smart plug or CT clamp on the EVSE circuit would be needed as a separate HA sensor.

---

### Octopus Energy (Agile Tariff + Gas)

#### Live Pricing (updates every 30 minutes)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_current_rate` | Import rate now | 30.84 p/kWh |
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_next_rate` | Import rate next slot | 27.21 p/kWh |
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_previous_rate` | Import rate last slot | 48.43 p/kWh |
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_current_standing_charge` | Electricity standing charge | 54.85 p/day |
| `sensor.octopus_energy_electricity_22l4344979_1170001806920_export_current_rate` | Export rate now | 14.59 p/kWh |
| `sensor.octopus_energy_electricity_22l4344979_1170001806920_export_next_rate` | Export rate next slot | 12.96 p/kWh |
| `sensor.octopus_energy_gas_e6e07422582221_2112316000_current_rate` | Gas rate | 5.99 p/kWh |
| `sensor.octopus_energy_gas_e6e07422582221_2112316000_current_standing_charge` | Gas standing charge | 33.46 p/day |

#### Yesterday's Metered Consumption & Cost (updates once daily from smart meter)

| Entity | Description | Yesterday |
|--------|-------------|-----------|
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_previous_accumulative_consumption` | Electricity imported | 17.56 kWh |
| `sensor.octopus_energy_electricity_22l4344979_1100009640372_previous_accumulative_cost` | Electricity import cost | £4.02 |
| `sensor.octopus_energy_electricity_22l4344979_1170001806920_export_previous_accumulative_consumption` | Electricity exported | 0.748 kWh |
| `sensor.octopus_energy_electricity_22l4344979_1170001806920_export_previous_accumulative_cost` | Export income | £0.05 |
| `sensor.octopus_energy_gas_e6e07422582221_2112316000_previous_accumulative_consumption_kwh` | Gas consumed | 11.12 kWh |
| `sensor.octopus_energy_gas_e6e07422582221_2112316000_previous_accumulative_consumption_m3` | Gas consumed (volume) | 0.979 m³ |
| `sensor.octopus_energy_gas_e6e07422582221_2112316000_previous_accumulative_cost` | Gas cost | £0.91 |

#### Rate Schedule Events (full day half-hourly slots as event attributes)

| Entity | Description |
|--------|-------------|
| `event.octopus_energy_electricity_22l4344979_1100009640372_current_day_rates` | Today's 48 import rate slots |
| `event.octopus_energy_electricity_22l4344979_1100009640372_next_day_rates` | Tomorrow's 48 import rate slots |
| `event.octopus_energy_electricity_22l4344979_1170001806920_export_current_day_rates` | Today's 48 export rate slots |
| `event.octopus_energy_electricity_22l4344979_1170001806920_export_next_day_rates` | Tomorrow's 48 export rate slots |
| `event.octopus_energy_gas_e6e07422582221_2112316000_current_day_rates` | Today's gas rates |

#### Account & Off-Peak Signals

| Entity | Description | Current |
|--------|-------------|---------|
| `binary_sensor.octopus_energy_electricity_22l4344979_1100009640372_off_peak` | Currently in off-peak window | off |
| `binary_sensor.octopus_energy_electricity_22l4344979_1170001806920_export_off_peak` | Export currently off-peak | off |
| `sensor.octopus_energy_a_808e2ce3_octoplus_points` | OctoPlus reward points | 84 |
| `calendar.octopus_energy_a_808e2ce3_octoplus_saving_sessions` | Saving session schedule | — |

#### Long-term Statistics (available for Energy Manager & monthly rollups)
These statistics IDs are used directly by HA's statistics engine — not regular entities:
- `octopus_energy:electricity_22l4344979_1100009640372_previous_accumulative_consumption`
- `octopus_energy:electricity_22l4344979_1100009640372_previous_accumulative_cost`
- `octopus_energy:electricity_22l4344979_1170001806920_export_previous_accumulative_consumption`
- `octopus_energy:electricity_22l4344979_1170001806920_export_previous_accumulative_cost`
- `octopus_energy:gas_e6e07422582221_2112316000_previous_accumulative_consumption_kwh`
- `octopus_energy:gas_e6e07422582221_2112316000_previous_accumulative_cost`

---

### Victron (Horsebox — Cerbo GX via Modbus TCP)

#### System Level (unit 100)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.victron_system_battery_soc` | Battery state of charge | 96% |
| `sensor.victron_system_battery_voltage` | Battery bank voltage | 13.5 V |
| `sensor.victron_system_battery_power` | Battery power (positive=charging) | 1 W |
| `sensor.victron_system_battery_current` | Battery current | 0.1 A |
| `sensor.victron_system_battery_state` | Battery state | IDLE / CHARGING / DISCHARGING |
| `sensor.victron_system_grid_l1` | Shore power draw | W |
| `sensor.victron_system_input_source` | Active power source | GRID / NOT_CONNECTED |
| `sensor.victron_system_consumption_l1` | AC loads | W |
| `sensor.victron_system_dc_pv_power` | DC solar power (system view) | W |
| `sensor.victron_system_bus_charge_power` | Total DC charge power | W |

#### MPPT Solar Charger (unit 223)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.victronsolarcharger_state223` | Charger state | EXTERNAL_CONTROL |
| `sensor.victronsolarcharger_yield_power223` | Solar power now | W |
| `sensor.victronsolarcharger_pv_voltage223` | PV panel voltage | 71.6 V |
| `sensor.victronsolarcharger_battery_current223` | Charge current to battery | A |
| `sensor.victronsolarcharger_battery_voltage223` | Battery voltage (at charger) | V |
| `sensor.victronsolarcharger_yield_today223` | Solar energy today | 0.2 kWh |
| `sensor.victronsolarcharger_yield_yesterday223` | Solar energy yesterday | 0.2 kWh |
| `sensor.victronsolarcharger_maxpower_today223` | Peak solar power today | 68 W |
| `sensor.victronsolarcharger_maxpower_yesterday223` | Peak solar power yesterday | 90 W |
| `sensor.victronsolarcharger_yield_user223` | Lifetime solar yield | 15 kWh |

#### VE.Bus Inverter / Charger (unit 227)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.victronvebus_state227` | Inverter/charger state | ABSORPTION / OFF |
| `sensor.victronvebus_charge_state227` | Charge stage | ABSORPTION / FLOAT / BULK |
| `sensor.victronvebus_activein_l1_voltage227` | Shore power voltage | 247 V |
| `sensor.victronvebus_activein_l1_current227` | Shore power current | A |
| `sensor.victronvebus_activein_l1_power227` | Shore power draw | W |
| `sensor.victronvebus_out_l1_voltage227` | AC output voltage | V |
| `sensor.victronvebus_out_l1_current227` | AC output current | A |
| `sensor.victronvebus_out_l1_power227` | AC output power | W |
| `sensor.victronvebus_activein_currentlimit227` | Shore current limit | 11 A |
| `sensor.victronvebus_battery_current227` | DC current from/to battery | A |
| `sensor.victronvebus_acin1toacout227` | Energy: shore → AC out (kWh) | kWh |
| `sensor.victronvebus_invertertoacout227` | Energy: battery → AC out (kWh) | kWh |

#### Alternator Charger (unit 224)

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.victronalternator_state224` | Charger state | OFF |
| `sensor.victronalternator_battery_voltage224` | Battery voltage | 13.52 V |
| `sensor.victronalternator_battery_current224` | Charge current | A |
| `sensor.victronalternator_input_voltage224` | Alternator voltage | 12.4 V |
| `sensor.victronalternator_engine_speed224` | Engine RPM | rpm |
| `sensor.victronalternator_cumulative_amp_hours_charged224` | Lifetime Ah charged | 614 Ah |

---

### UK Carbon Intensity (HACS: carbon_intensity_uk v0.0.3)

Real-time UK grid carbon intensity data from the National Grid ESO Carbon Intensity API. Updates automatically; all sensors have `state_class: measurement` so HA records history.

| Entity | Description | Current |
|--------|-------------|---------|
| `sensor.carbon_intensity_regional` | Regional grid carbon intensity | 288 gCO2eq/kWh |
| `sensor.carbon_intensity_regional_fossil_fuel_percentage` | Fossil fuel share of regional generation | 86.1% |
| `sensor.carbon_intensity_regional_green_fuel_percentage` | Green/renewable share of regional generation | 13.1% |

**Use cases:**
- Overlay on the efficiency dashboard to show whether grid imports happened during high or low carbon periods
- Weight the energy score by carbon intensity — importing during low-carbon periods is better than importing during high-carbon periods even at the same price
- Track daily/weekly carbon intensity trends to understand seasonal green energy availability
- Combine with `solax_grid_import` to estimate carbon footprint of grid consumption: `import_kWh × gCO2eq/kWh`