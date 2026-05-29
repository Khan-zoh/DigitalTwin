from dataclasses import dataclass


@dataclass(frozen=True)
class SimConfig:
    horizon_days: int = 365
    warmup_days: int = 28
    target_service_level: float = 0.95
    random_seed: int = 42
    output_db_path: str = "data/output/scenario_results.duckdb"
    seed_data_dir: str = "data/seed"
