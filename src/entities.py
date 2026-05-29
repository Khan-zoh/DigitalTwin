from dataclasses import dataclass


@dataclass(frozen=True)
class SKU:
    sku_id: str
    name: str
    unit_cost: float
    unit_price: float
    holding_cost_per_week: float
    backorder_penalty: float
    component_a_qty: int
    component_b_qty: int


@dataclass(frozen=True)
class Supplier:
    supplier_id: str
    component: str
    unit_cost: float
    lead_time_mean_days: int
    lead_time_std_days: float
    reliability: float
    max_weekly_capacity: int
    co2_per_unit_kg: float


@dataclass(frozen=True)
class DistributionCenter:
    dc_id: str
    name: str
    storage_capacity: int
    weekly_throughput_capacity: int
    holding_cost_multiplier: float


@dataclass(frozen=True)
class CustomerRegion:
    region_id: str
    primary_dc: str
    secondary_dc: str
    transport_cost_primary: float
    transport_cost_secondary: float
    transport_co2_primary_kg: float
    transport_co2_secondary_kg: float


@dataclass(frozen=True)
class Order:
    order_id: str
    day: int
    region_id: str
    sku_id: str
    quantity: int


@dataclass(frozen=True)
class Shipment:
    shipment_id: str
    day: int
    origin_id: str
    destination_id: str
    sku_id: str
    quantity: int
    cost: float
    co2_kg: float
