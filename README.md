# Supply Chain Digital Twin

Discrete-event simulation of a 3-tier supply network with optimization, disruption scenarios, KPI tracking, and dashboards.

This project models how products move from suppliers, to a factory, to distribution centers, and finally to customer regions. The purpose is to test how the supply chain performs under normal operations and under disruption, then use the results to support better planning decisions.

## V1 Project Scope

V1 is the first complete version of the project. It focuses on building an end-to-end supply chain digital twin that can run reproducible scenarios, measure operational performance, and display the results in dashboards.

The supply chain model includes:

- 3 suppliers
- 1 factory
- 2 distribution centers
- 4 customer regions
- 5 SKUs
- 52-week simulation horizon
- Daily simulation time steps

The system follows this flow:

```text
Suppliers -> Factory -> Distribution Centers -> Customer Regions
```

V1 will answer questions such as:

- What happens when a key supplier goes down?
- What happens when customer demand suddenly spikes?
- How much inventory is needed to protect service levels?
- Which scenarios increase cost the most?
- Which disruptions hurt fill rate and OTIF the most?
- How do cost, service, and CO2 emissions change across scenarios?

## V1 Core Components

### Seed Data

The project will generate deterministic seed data for:

- SKUs
- suppliers
- distribution centers
- customer regions
- weekly demand profiles

The data generation process will use fixed random seeds so the same inputs can be recreated every time.

### Simulation

The simulation will use SimPy to model daily supply chain operations.

It will track:

- supplier lead times
- supplier reliability
- component arrivals
- factory production
- DC inventory
- customer demand
- fulfilled orders
- stockouts
- transportation events
- costs
- CO2 emissions

All activity will be written to an event log for KPI calculation and analysis.

### Optimization

V1 includes two optimization models using PuLP:

- Production planning optimization
- Transportation allocation optimization

These models help decide what to produce and how to allocate shipments while considering capacity, demand, cost, and inventory constraints.

### Scenarios

V1 will run five scenarios:

- Baseline
- Supplier outage
- Demand spike
- Long lead time
- Combined stress

These scenarios are designed to test how resilient the supply chain is under different operating conditions.

### KPIs

V1 will calculate:

- Fill rate
- OTIF
- Days of supply
- Inventory turns
- Total landed cost
- Stockout events
- Total CO2 kg
- Revenue
- Gross margin %

The results will be stored in DuckDB so they can be used by dashboards and analysis tools.

### Dashboards

V1 will include:

- Streamlit dashboard
- Power BI dashboard

The Streamlit dashboard will show:

- scenario picker
- KPI cards
- scenario comparison charts
- inventory time series
- cost breakdowns

The Power BI dashboard will reproduce the main KPI views and include an additional sustainability quadrant showing cost vs. CO2 by scenario.

## V1 Success Criteria

V1 is complete when:

- `python -m src.run_all --scenario baseline` runs successfully
- all five scenarios run successfully
- results are written to `data/output/scenario_results.duckdb`
- Streamlit dashboard launches and displays the required visuals
- Power BI dashboard is created
- `pytest tests/` passes
- README includes setup instructions, architecture, screenshots, and resume-ready bullets

## Current Project Status

The current repository contains the initial scaffold:

- pinned Python dependencies
- pytest configuration
- source package folder
- tests folder
- data folders
- dashboard folder
- git repository connected to GitHub

The next implementation step is Phase 2: deterministic seed data generation.

## V1 Build Plan

### Phase 1: Foundation

- Create the project structure
- Set up Python 3.11 virtual environment
- Install pinned dependencies
- Verify core packages import correctly
- Verify PuLP CBC solver is available

### Phase 2: Seed Data

- Build `src/config.py`
- Build `src/entities.py`
- Build `src/data_gen.py`
- Generate the five seed CSV files
- Add tests for schema, row counts, and deterministic generation

### Phase 3: Simulation

- Build the event log
- Simulate customer demand
- Simulate DC fulfillment
- Simulate stockouts
- Add factory production
- Add supplier lead times and reliability
- Add simulation tests

### Phase 4: Optimization

- Build the production planning LP
- Build the transportation LP
- Test both optimizers with small known examples
- Connect the optimization outputs to the simulation

### Phase 5: KPIs and Scenarios

- Build KPI calculations
- Build scenario configuration
- Build the command-line runner
- Write results to DuckDB
- Confirm scenario results differ meaningfully

### Phase 6: Dashboards

- Build the Streamlit dashboard
- Export CSV outputs for Power BI
- Build the Power BI report manually
- Save a dashboard screenshot

### Phase 7: Polish

- Complete README documentation
- Add architecture diagram
- Add screenshots
- Add resume-ready bullets
- Run all tests
- Push the completed v1 to GitHub

## Future Enhancements After V1

These are not part of v1. They are the next steps to make the project more advanced after the original specification is complete.

### Monte Carlo Simulation

Run each scenario many times with different random seeds instead of running each scenario once.

This would allow the project to measure:

- average performance
- worst-case performance
- confidence intervals
- probability of stockout
- probability of missing service-level targets
- expected cost under uncertainty

This would turn the project from a single-scenario simulator into a risk analysis tool.

### Advanced Bottleneck Metrics

Add deeper utilization metrics across the supply chain.

Possible metrics:

- supplier capacity utilization
- factory capacity utilization
- DC throughput utilization
- DC storage utilization
- bottleneck frequency
- constrained weeks by node

This would help identify where the supply chain is most likely to break under stress.

### Backorder Aging and Lost Sales

V1 tracks stockouts, but a more advanced version should distinguish between delayed demand and permanently lost demand.

Future metrics:

- average backorder age
- maximum backorder age
- lost sales units
- lost sales revenue
- customer wait time
- service recovery time

This would make the customer-service side of the model more realistic.

### Demand Forecasting Layer

Add a forecasting model that predicts future demand and feeds the production planning optimizer.

Possible forecasting methods:

- moving average
- exponential smoothing
- seasonal naive forecast
- Prophet
- machine learning forecast model

Forecasting metrics could include:

- WAPE
- MAPE
- forecast bias
- forecast error by SKU
- forecast error by region

This would let the project show how forecast quality affects inventory, service, and cost.

### Resilience Score

Create a single score that summarizes how well the supply chain survives disruption.

The score could combine:

- fill rate under disruption
- OTIF under disruption
- recovery time
- cost increase
- stockout severity
- supplier concentration risk
- emissions impact

This would make scenario comparison easier for a business audience.

### Fourth Tier: Raw Material Suppliers

Expand the network from:

```text
Suppliers -> Factory -> Distribution Centers -> Customer Regions
```

to:

```text
Raw Material Suppliers -> Component Suppliers -> Factory -> Distribution Centers -> Customer Regions
```

This would allow the project to model upstream risk, where a supplier may fail because its own raw material supply is constrained.

### Multi-Echelon Safety Stock Optimization

Replace the simple safety stock grid search with a more advanced optimization approach.

This would decide where inventory should be held across the network:

- upstream raw materials
- components
- finished goods at factory
- finished goods at DCs

The goal would be to hit service targets at the lowest total inventory cost.

### Interactive What-If Dashboard

Add dashboard controls that let a user change assumptions and compare results.

Possible controls:

- demand multiplier
- lead time multiplier
- supplier reliability
- factory capacity
- DC capacity
- service-level target
- carbon cost per kg

This would make the project feel more like a decision-support tool.

### Sustainability and Carbon Costing

Expand the CO2 analysis by adding a carbon price.

Future metrics:

- carbon cost
- emissions by supplier
- emissions by transport lane
- emissions per fulfilled unit
- cost vs. emissions tradeoff

This would make the project stronger for companies focused on sustainable operations.

## Long-Term Vision

The long-term goal is to evolve this from a v1 portfolio simulation into a supply chain risk intelligence tool.

V1 shows what happens across a few planned scenarios. Future versions should show how likely bad outcomes are, where the system is most vulnerable, and which decisions improve resilience, cost, service, and sustainability.
