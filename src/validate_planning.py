
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASTER = PROJECT_ROOT / "data" / "master"
TRANS = PROJECT_ROOT / "data" / "transactions"
OUTPUT = PROJECT_ROOT / "data" / "ground_truth"

# Load files
skus = pd.read_csv(MASTER / "skus.csv")
locations = pd.read_csv(MASTER / "locations.csv")
suppliers = pd.read_csv(MASTER / "suppliers.csv")

demand = pd.read_csv(TRANS / "forecast_demand.csv")
inventory = pd.read_csv(TRANS / "inventory.csv")
capacity = pd.read_csv(TRANS / "supplier_capacity.csv")
lead_times = pd.read_csv(TRANS / "lead_times.csv")
pos = pd.read_csv(TRANS / "purchase_orders.csv")
production = pd.read_csv(TRANS / "production_plans.csv")

pab = pd.read_csv(OUTPUT / "pab_results.csv")
shortages = pd.read_csv(OUTPUT / "shortages.csv")
mitigations = pd.read_csv(OUTPUT / "mitigation_options.csv")

print("\nADVANCED DATA VALIDATION")
print("------------------------")

# 1. Primary key checks
print("Duplicate SKU IDs:", skus["sku_id"].duplicated().sum())
print("Duplicate Location IDs:", locations["location_id"].duplicated().sum())
print("Duplicate Supplier IDs:", suppliers["supplier_id"].duplicated().sum())
print("Duplicate Shortage IDs:", shortages["shortage_id"].duplicated().sum())

# 2. Foreign key checks
print("Invalid demand SKU references:",
      (~demand["sku_id"].isin(skus["sku_id"])).sum())

print("Invalid demand location references:",
      (~demand["location_id"].isin(locations["location_id"])).sum())

print("Invalid inventory SKU references:",
      (~inventory["sku_id"].isin(skus["sku_id"])).sum())

print("Invalid PO supplier references:",
      (~pos["supplier_id"].isin(suppliers["supplier_id"])).sum())

print("Invalid mitigation shortage references:",
      (~mitigations["shortage_id"].isin(shortages["shortage_id"])).sum())

# 3. Quantity checks
print("Negative forecast quantities:",
      (demand["forecast_quantity"] < 0).sum())

print("Negative inventory quantities:",
      ((inventory["on_hand_quantity"] < 0) |
       (inventory["inbound_quantity"] < 0)).sum())

print("Negative purchase order quantities:",
      (pos["order_quantity"] < 0).sum())

# 4. Supplier capacity checks
capacity_check = pos.merge(
    capacity,
    on=["supplier_id", "sku_id"],
    how="left"
)

print("POs without matching capacity:",
      capacity_check["max_quantity"].isna().sum())

print("POs above supplier capacity:",
      (capacity_check["order_quantity"] >
       capacity_check["max_quantity"]).sum())

print("POs below minimum order quantity:",
      (capacity_check["order_quantity"] <
       capacity_check["min_order_quantity"]).sum())

# 5. Lead time checks
lead_check = pos.merge(
    lead_times,
    on=["supplier_id", "sku_id"],
    how="left"
)

print("POs without lead time:",
      lead_check["lead_time_days"].isna().sum())

# 6. Output consistency
print("PAB rows:", len(pab))
print("Shortage rows:", len(shortages))
print("Mitigation rows:", len(mitigations))

print("\nADVANCED VALIDATION COMPLETED")
