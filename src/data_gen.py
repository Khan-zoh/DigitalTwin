from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import SimConfig


SKU_ROWS = [
    {
        "sku_id": "SKU001",
        "name": "Widget A",
        "unit_cost": 12.50,
        "unit_price": 26.00,
        "holding_cost_per_week": 0.30,
        "backorder_penalty": 3.00,
        "component_a_qty": 1,
        "component_b_qty": 2,
        "base_weekly_demand": 260,
    },
    {
        "sku_id": "SKU002",
        "name": "Widget B",
        "unit_cost": 15.00,
        "unit_price": 31.00,
        "holding_cost_per_week": 0.35,
        "backorder_penalty": 3.50,
        "component_a_qty": 2,
        "component_b_qty": 1,
        "base_weekly_demand": 220,
    },
    {
        "sku_id": "SKU003",
        "name": "Widget C",
        "unit_cost": 9.00,
        "unit_price": 18.00,
        "holding_cost_per_week": 0.24,
        "backorder_penalty": 2.25,
        "component_a_qty": 1,
        "component_b_qty": 1,
        "base_weekly_demand": 70,
    },
    {
        "sku_id": "SKU004",
        "name": "Widget D",
        "unit_cost": 18.00,
        "unit_price": 34.00,
        "holding_cost_per_week": 0.42,
        "backorder_penalty": 4.00,
        "component_a_qty": 2,
        "component_b_qty": 2,
        "base_weekly_demand": 55,
    },
    {
        "sku_id": "SKU005",
        "name": "Widget E",
        "unit_cost": 7.50,
        "unit_price": 15.50,
        "holding_cost_per_week": 0.20,
        "backorder_penalty": 2.00,
        "component_a_qty": 1,
        "component_b_qty": 0,
        "base_weekly_demand": 45,
    },
]


SUPPLIER_ROWS = [
    {
        "supplier_id": "SUP01",
        "component": "component_a",
        "unit_cost": 1.20,
        "lead_time_mean_days": 7,
        "lead_time_std_days": 1.5,
        "reliability": 0.86,
        "max_weekly_capacity": 5000,
        "co2_per_unit_kg": 0.04,
    },
    {
        "supplier_id": "SUP02",
        "component": "component_b",
        "unit_cost": 1.45,
        "lead_time_mean_days": 9,
        "lead_time_std_days": 2.0,
        "reliability": 0.94,
        "max_weekly_capacity": 4500,
        "co2_per_unit_kg": 0.05,
    },
    {
        "supplier_id": "SUP03",
        "component": "component_a,component_b",
        "unit_cost": 1.75,
        "lead_time_mean_days": 5,
        "lead_time_std_days": 1.2,
        "reliability": 0.97,
        "max_weekly_capacity": 3000,
        "co2_per_unit_kg": 0.06,
    },
]


DC_ROWS = [
    {
        "dc_id": "DC01",
        "name": "Coastal DC",
        "storage_capacity": 20000,
        "weekly_throughput_capacity": 8000,
        "holding_cost_multiplier": 1.00,
    },
    {
        "dc_id": "DC02",
        "name": "Inland DC",
        "storage_capacity": 18000,
        "weekly_throughput_capacity": 7500,
        "holding_cost_multiplier": 1.10,
    },
]


CUSTOMER_ROWS = [
    {
        "region_id": "REG_NE",
        "primary_dc": "DC01",
        "secondary_dc": "DC02",
        "transport_cost_primary": 0.45,
        "transport_cost_secondary": 0.90,
        "transport_co2_primary_kg": 0.12,
        "transport_co2_secondary_kg": 0.25,
    },
    {
        "region_id": "REG_SE",
        "primary_dc": "DC01",
        "secondary_dc": "DC02",
        "transport_cost_primary": 0.42,
        "transport_cost_secondary": 0.88,
        "transport_co2_primary_kg": 0.11,
        "transport_co2_secondary_kg": 0.24,
    },
    {
        "region_id": "REG_MW",
        "primary_dc": "DC02",
        "secondary_dc": "DC01",
        "transport_cost_primary": 0.40,
        "transport_cost_secondary": 0.84,
        "transport_co2_primary_kg": 0.10,
        "transport_co2_secondary_kg": 0.22,
    },
    {
        "region_id": "REG_W",
        "primary_dc": "DC02",
        "secondary_dc": "DC01",
        "transport_cost_primary": 0.50,
        "transport_cost_secondary": 0.95,
        "transport_co2_primary_kg": 0.14,
        "transport_co2_secondary_kg": 0.28,
    },
]


REGION_DEMAND_WEIGHTS = {
    "REG_NE": 0.30,
    "REG_SE": 0.27,
    "REG_MW": 0.25,
    "REG_W": 0.18,
}


def generate_skus() -> pd.DataFrame:
    df = pd.DataFrame(SKU_ROWS)
    return df.drop(columns=["base_weekly_demand"])


def generate_suppliers() -> pd.DataFrame:
    return pd.DataFrame(SUPPLIER_ROWS)


def generate_dcs() -> pd.DataFrame:
    return pd.DataFrame(DC_ROWS)


def generate_customers() -> pd.DataFrame:
    return pd.DataFrame(CUSTOMER_ROWS)


def generate_demand_profile() -> pd.DataFrame:
    rng = np.random.default_rng(SimConfig().random_seed)
    rows = []

    for week in range(1, 53):
        seasonal_signal = np.sin(2 * np.pi * (week - 17) / 52)
        seasonality_factor = 1.0 + 0.18 * seasonal_signal
        trend_factor = 1 + 0.005 * week

        for region_id, region_weight in REGION_DEMAND_WEIGHTS.items():
            for sku in SKU_ROWS:
                noise = rng.normal(1.0, 0.025)
                mean_demand = sku["base_weekly_demand"] * region_weight * noise
                rows.append(
                    {
                        "week": week,
                        "region_id": region_id,
                        "sku_id": sku["sku_id"],
                        "mean_demand": round(float(mean_demand), 2),
                        "seasonality_factor": round(float(seasonality_factor), 4),
                        "trend_factor": round(float(trend_factor), 4),
                    }
                )

    return pd.DataFrame(rows)


def generate_all(config: SimConfig | None = None) -> None:
    config = config or SimConfig()
    random.seed(config.random_seed)
    np.random.seed(config.random_seed)

    output_dir = Path(config.seed_data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "skus.csv": generate_skus(),
        "suppliers.csv": generate_suppliers(),
        "dcs.csv": generate_dcs(),
        "customers.csv": generate_customers(),
        "demand_profile.csv": generate_demand_profile(),
    }

    for file_name, df in files.items():
        df.to_csv(output_dir / file_name, index=False)


if __name__ == "__main__":
    generate_all()
