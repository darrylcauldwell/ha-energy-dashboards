# Perfect Home Energy Dashboard Architecture

This document defines the complete end-state design for an outcome-driven Home Assistant energy system. All dashboards are fully specified with predictive, carbon-aware, and optimisation capabilities.

---

# Dashboard 1 — Live Energy Command Centre

## Purpose  
Real-time operational awareness and immediate intervention decisions.

## User should know instantly

- Current energy flow direction  
- Whether now is cheap to consume  
- Whether now is low carbon  
- Whether the battery is behaving optimally  
- Whether house load is abnormal  

---

## Layout Specification

### Section A — Power Flow (primary visual)

**Card:** `custom:power-flow-card-plus`

**Entities**

- Solar: `sensor.solax_pv_power_total`
- Battery: `sensor.solax_battery_power_charge`
- Grid (net): template (import − export)
- Home: `sensor.solax_house_load`

**Enhancements**

- Colour by flow direction  
- Battery colour by charge/discharge  
- Grid colour by import/export  

---

### Section B — Real-Time Decision Strip

Compact chip row.

**Required chips**

1. Battery state  
   - SOC  
   - charge/discharge state  
   - time-to-empty/full estimate (derived)

2. Import price now  
   - current rate  
   - percentile vs today’s rates (derived)  
   - highlight if in cheapest quartile  

3. Carbon intensity now  
   - gCO₂/kWh  
   - banded colour (low/medium/high)  
   - percentile vs today  

4. House load  
   - current W  
   - deviation from rolling 7-day baseline  

5. Composite opportunity indicator (derived)

**States**

- OPTIMAL TO USE POWER  
- NEUTRAL  
- AVOID USE  

(Based on price + carbon + solar surplus)

---

### Section C — Intraday Performance

**Today so far**

- Solar produced  
- Grid imported  
- Grid exported  
- Battery net throughput  
- Running import cost  
- Running export revenue  
- Running carbon emitted  
- Running carbon avoided  

(All continuously updated)

---

### Section D — System Intent and Constraints

**Show full control state**

- inverter run mode  
- charger use mode  
- charge/discharge windows  
- night charge enabled  
- night charge ceiling  
- discharge minimum SOC  
- EV charger mode and limit  

**Enhancement**

- Warning highlighting when settings conflict with forecast optimisation

---

### Section E — Live Anomaly Detection

Derived alerts:

- unexpected grid import while solar available  
- battery idle during cheap period  
- unusually high baseload  
- export while battery below target SOC  

Display as alert list.

---

---

# Dashboard 2 — Optimisation and Forward Strategy

## Purpose  
Drive daily optimisation behaviour and quantify lost opportunity.

## User should know instantly

- How well the system performed today  
- Where money/carbon was lost  
- What to change tonight  
- Whether tomorrow requires a different battery strategy  

---

## Layout Specification

### Section A — Composite Performance Score

Single score: **0–100**

**Weights**

- solar self-consumption efficiency  
- cheap import alignment  
- export value capture  
- carbon efficiency  
- battery cycle efficiency  

Display main score plus all sub-scores.

---

### Section B — Missed Opportunity Engine

Daily calculated counterfactuals:

- Battery timing loss (£)  
- Export timing loss (£)  
- Solar spill loss (£ and kWh)  
- Carbon timing penalty (kgCO₂ above optimal)  
- Avoidable peak import (kWh)  

Also show rolling 7-day total.

---

### Section C — Charging Alignment Analysis

**Graph overlay**

- battery SOC  
- import price  
- carbon intensity  

**Derived metric**

- % of charging done in optimal windows

---

### Section D — Next 24-Hour Plan

Natural-language summary generated from templates.

**Inputs**

- next-day Agile rates  
- carbon forecast  
- solar forecast  
- current SOC  
- usable battery capacity  
- typical overnight load  
- weather confidence  

**Outputs**

- cheapest charge window  
- lowest carbon window  
- expected solar production  
- recommended night charge ceiling  
- recommended charge window times  
- expected export tomorrow  
- estimated financial impact  
- estimated carbon impact  
- confidence level  

---

### Section E — Battery Strategy Advisor

**Classification**

- Strong surplus day  
- Mild surplus  
- Neutral  
- Deficit  
- Heavy deficit  

**Recommendations**

- night charge SOC  
- discharge floor  
- whether to enable extra charge window  

---

### Section F — Flexible Load Intelligence

Automatic detection of major loads.

**Daily breakdown**

- EV charging energy  
- dishwasher/washing spikes  
- immersion or heater events  
- abnormal overnight baseload  

**Derived metric**

- Shiftable load opportunity (kWh)

---

### Section G — Automation Readiness

Status indicators:

- battery auto-optimisation (ON/OFF)  
- EV solar mode (ON/OFF)  
- peak avoidance automation (ON/OFF)  

Purpose: close the loop between insight and action.

---

---

# Dashboard 3 — Financial and Carbon Outcomes

## Purpose  
Monthly accountability and long-term trend tracking.

## User should know instantly

- projected monthly bill  
- how much export offsets costs  
- standing charge burden  
- carbon footprint trajectory  
- whether optimisation is improving over time  

---

## Layout Specification

### Section A — Month-to-Date Financial Summary

**Cards**

- electricity import cost  
- export revenue  
- gas cost  
- standing charges total  
- net energy cost  
- projected end-of-month bill (forecast)

Projection uses run-rate model.

---

### Section B — Cost Composition

Percentage breakdown:

- import energy  
- gas  
- standing charges  
- export offset  

Include stacked visual.

---

### Section C — Daily Cost Timeline

30-day chart:

- import cost  
- gas cost  
- export income  
- net daily cost  

---

### Section D — Carbon Accounting

Month-to-date:

- total kgCO₂  
- grid carbon average  
- solar avoided carbon  
- battery carbon benefit (derived)  

Optional:

- comparison vs regional or national intensity

---

### Section E — Trend Analysis

Rolling metrics:

- cost per kWh over time  
- self-consumption trend  
- import during peak trend  
- carbon per kWh trend  

Purpose: verify optimisation improvements.

---

### Section F — Standing Charge Impact Analysis

Explicit visibility:

- standing charges vs energy spend  
- projected annual standing cost  
- percentage of total bill  

---

---

# Dashboard 4 — Horsebox Energy Intelligence

## Purpose  
Full off-grid energy intelligence and trip efficiency.

## User should know instantly

- current power source  
- off-grid endurance  
- solar contribution  
- alternator contribution  
- trip energy performance  
- self-sufficiency level  

---

## Layout Specification

### Section A — Horsebox Power Flow

Visual flow showing:

- solar  
- battery  
- shore  
- loads  
- alternator  

Use derived net flows where necessary.

---

### Section B — Live Status Strip

Show:

- battery SOC  
- battery power  
- active input source  
- AC load  
- solar power  
- time-to-empty estimate  

---

### Section C — Energy Source Breakdown

Daily and trip totals:

- solar kWh  
- shore kWh  
- alternator kWh  
- battery discharge kWh  

Also show percentages.

---

### Section D — Self-Sufficiency Score

Composite metric:

- percent of load met by solar + alternator  
- shore dependence index  
- days fully off-grid  

Primary KPI for mobile system.

---

### Section E — Trip Energy Log

Automatic trip detection using:

- engine RPM  
- alternator activity  
- shore disconnect  

**Per-trip summary**

- duration  
- alternator Ah added  
- solar during trip  
- net battery delta  
- energy per mile (if odometer available)

---

### Section F — Off-Grid Endurance Predictor

Forecast:

- hours remaining at current load  
- overnight survivability  
- minimum SOC by morning  

Based on:

- rolling load average  
- battery usable capacity  
- solar forecast (optional)

---

### Section G — System Health

Monitor and alert:

- battery temperature  
- charge stage  
- abnormal voltage  
- charger state anomalies  

---

---

# System Architecture Summary

**Dashboard roles**

1. Command Centre — real-time decisions  
2. Optimisation — daily behaviour change  
3. Financial & Carbon — long-term outcomes  
4. Horsebox Intelligence — mobile energy mastery  

**Closed loop**

measure → evaluate → predict → recommend → verify