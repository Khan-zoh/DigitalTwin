from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import SimConfig
from src.data_gen import generate_all


EXPECTED_COLUMNS = {
    "skus.csv": [
        "sku_id",
        "name",
        "unit_cost",
        "unit_price",
        "holding_cost_per_week",
        "backorder_penalty",
        "component_a_qty",
        "component_b_qty",
    ],
    "suppliers.csv": [
        "supplier_id",
        "component",
        "unit_cost",
        "lead_time_mean_days",
        "lead_time_std_days",
        "reliability",
        "max_weekly_capacity",
        "co2_per_unit_kg",
    ],
    "dcs.csv": [
        "dc_id",
        "name",
        "storage_capacity",
        "weekly_throughput_capacity",
        "holding_cost_multiplier",
    ],
    "customers.csv": [
        "region_id",
        "primary_dc",
        "secondary_dc",
        "transport_cost_primary",
        "transport_cost_secondary",
        "transport_co2_primary_kg",
        "transport_co2_secondary_kg",
    ],
    "demand_profile.csv": [
        "week",
        "region_id",
        "sku_id",
        "mean_demand",
        "seasonality_factor",
        "trend_factor",
    ],
}


EXPECTED_ROW_COUNTS = {
    "skus.csv": 5,
    "suppliers.csv": 3,
    "dcs.csv": 2,
    "customers.csv": 4,
    "demand_profile.csv": 52 * 4 * 5,
}


def _config(tmp_path: Path) -> SimConfig:
    return SimConfig(seed_data_dir=str(tmp_path))


def test_generate_all_writes_expected_files(tmp_path: Path) -> None:
    generate_all(_config(tmp_path))

    for file_name in EXPECTED_COLUMNS:
        assert (tmp_path / file_name).exists()


def test_schemas_and_row_counts(tmp_path: Path) -> None:
    generate_all(_config(tmp_path))

    for file_name, expected_columns in EXPECTED_COLUMNS.items():
        df = pd.read_csv(tmp_path / file_name)
        assert list(df.columns) == expected_columns
        assert len(df) == EXPECTED_ROW_COUNTS[file_name]


def test_generation_is_idempotent(tmp_path: Path) -> None:
    config = _config(tmp_path)

    generate_all(config)
    first_run = {
        file_name: (tmp_path / file_name).read_text()
        for file_name in EXPECTED_COLUMNS
    }

    generate_all(config)
    second_run = {
        file_name: (tmp_path / file_name).read_text()
        for file_name in EXPECTED_COLUMNS
    }

    assert first_run == second_run


def test_supplier_outage_scenario_has_unreliable_supplier(tmp_path: Path) -> None:
    generate_all(_config(tmp_path))

    suppliers = pd.read_csv(tmp_path / "suppliers.csv")
    assert (suppliers["reliability"] < 0.90).any()


def test_demand_profile_has_full_week_region_sku_grid(tmp_path: Path) -> None:
    generate_all(_config(tmp_path))

    demand = pd.read_csv(tmp_path / "demand_profile.csv")
    grid_size = demand[["week", "region_id", "sku_id"]].drop_duplicates().shape[0]

    assert demand["week"].min() == 1
    assert demand["week"].max() == 52
    assert grid_size == 52 * 4 * 5
