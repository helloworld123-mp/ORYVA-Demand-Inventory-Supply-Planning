
# ORYVA - Demand, Inventory and Supply Planning
# Synthetic Data Generator

import random
import csv
from pathlib import Path
from datetime import date, timedelta

# 1. Fixed random seed
SEED = 20261022
random.seed(SEED)

# 2. Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 3. Output folders
MASTER_FOLDER = PROJECT_ROOT / "data" / "master"
TRANSACTION_FOLDER = PROJECT_ROOT / "data" / "transactions"

MASTER_FOLDER.mkdir(parents=True, exist_ok=True)
TRANSACTION_FOLDER.mkdir(parents=True, exist_ok=True)

# 4. Starter configuration
CONFIG = {
    "skus": 10,
    "locations": 3,
    "suppliers": 10,
    "weeks": 52,
}

# 5. Save CSV files
def save_csv(folder, filename, records):
    if not records:
        print("No records generated:", filename)
        return

    file_path = folder / filename

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print("Created:", file_path)

# 6. Generate SKU master data
def generate_skus():
    categories = ["Electronics", "Clothing", "Food", "Furniture"]
    units = ["PCS", "BOX", "KG"]
    records = []

    for i in range(1, CONFIG["skus"] + 1):
        records.append({
            "sku_id": f"SKU-{i:06d}",
            "product_name": f"Product {i}",
            "category": random.choice(categories),
            "unit": random.choice(units),
            "status": "Active"
        })

    return records

# 7. Generate Location master data
def generate_locations():
    cities = ["Bengaluru", "Chennai", "Mumbai"]
    states = ["Karnataka", "Tamil Nadu", "Maharashtra"]
    records = []

    for i in range(1, CONFIG["locations"] + 1):
        records.append({
            "location_id": f"LOC-{i:06d}",
            "location_name": f"Warehouse {i}",
            "city": cities[i - 1],
            "state": states[i - 1],
            "status": "Active"
        })

    return records

# 8. Generate Supplier master data
def generate_suppliers():
    records = []

    for i in range(1, CONFIG["suppliers"] + 1):
        records.append({
            "supplier_id": f"SUP-{i:06d}",
            "supplier_name": f"Supplier {i}",
            "contact_email": f"supplier{i}@example.com",
            "status": "Active"
        })

    return records

# 9. Generate Forecast Demand
def generate_forecast_demand(skus, locations):
    records = []
    start_date = date(2026, 1, 5)

    for sku in skus:
        for location in locations:
            for week in range(CONFIG["weeks"]):
                week_date = start_date + timedelta(weeks=week)

                records.append({
                    "demand_id": (
                        f"DEM-{sku['sku_id']}-"
                        f"{location['location_id']}-2026W{week + 1:02d}"
                    ),
                    "sku_id": sku["sku_id"],
                    "location_id": location["location_id"],
                    "week": f"2026W{week + 1:02d}",
                    "forecast_quantity": random.randint(20, 150),
                    "created_date": str(week_date)
                })

    return records

# 10. Generate Inventory
def generate_inventory(skus, locations):
    records = []

    for sku in skus:
        for location in locations:
            records.append({
                "inventory_id": (
                    f"INV-{sku['sku_id']}-{location['location_id']}"
                ),
                "sku_id": sku["sku_id"],
                "location_id": location["location_id"],
                "on_hand_quantity": random.randint(50, 300),
                "inbound_quantity": 0,
                "as_of_date": "2026-01-04"
            })

    return records

# 11. Generate Supplier Capacity
def generate_supplier_capacity(skus, suppliers):
    records = []

    for supplier in suppliers:
        for sku in random.sample(skus, 5):
            records.append({
                "capacity_id": (
                    f"CAP-{supplier['supplier_id']}-{sku['sku_id']}"
                ),
                "supplier_id": supplier["supplier_id"],
                "sku_id": sku["sku_id"],
                "max_quantity": random.randint(200, 1000),
                "min_order_quantity": random.choice([10, 20, 50]),
                "effective_from": "2026-01-01",
                "effective_to": "2026-12-31"
            })

    return records

# 12. Generate Lead Times
def generate_lead_times(skus, suppliers):
    records = []

    for supplier in suppliers:
        for sku in random.sample(skus, 5):
            records.append({
                "lead_time_id": (
                    f"LT-{supplier['supplier_id']}-{sku['sku_id']}"
                ),
                "supplier_id": supplier["supplier_id"],
                "sku_id": sku["sku_id"],
                "lead_time_days": random.randint(3, 21),
                "effective_from": "2026-01-01",
                "effective_to": "2026-12-31"
            })

    return records



# 11. Generate Purchase Orders

def generate_purchase_orders(skus, locations, suppliers, capacity, lead_times):
    records = []
    start_date = date(2026, 1, 1)

    for i in range(1, 31):
        sku = random.choice(skus)
        location = random.choice(locations)

        eligible = []

        for item in capacity:
            if item["sku_id"] != sku["sku_id"]:
                continue

            matching_lead_time = next(
                (
                    lt for lt in lead_times
                    if lt["supplier_id"] == item["supplier_id"]
                    and lt["sku_id"] == sku["sku_id"]
                ),
                None
            )

            if matching_lead_time is not None:
                eligible.append((item, matching_lead_time))

        if not eligible:
            continue

        selected_capacity, lead_time = random.choice(eligible)

        supplier = next(
            s for s in suppliers
            if s["supplier_id"] == selected_capacity["supplier_id"]
        )

        order_quantity = random.randint(
            int(selected_capacity["min_order_quantity"]),
            int(selected_capacity["max_quantity"])
        )

        order_date = start_date + timedelta(days=random.randint(0, 180))
        delivery_date = order_date + timedelta(
            days=int(lead_time["lead_time_days"])
        )

        records.append({
            "po_id": f"PO-2026-{i:06d}",
            "supplier_id": supplier["supplier_id"],
            "sku_id": sku["sku_id"],
            "location_id": location["location_id"],
            "order_quantity": order_quantity,
            "order_date": str(order_date),
            "expected_delivery_date": str(delivery_date),
            "received_quantity": 0,
            "status": "Open"
        })

    return records


# 12. Generate Production Plans

def generate_production_plans(skus, locations):
    records = []

    for i, sku in enumerate(skus, start=1):
        for location in locations:
            planned_quantity = random.randint(50, 200)
            production_capacity = random.randint(200, 300)

            start_date = date(2026, 1, 1) + timedelta(
                days=random.randint(0, 180)
            )
            end_date = start_date + timedelta(days=7)

            records.append({
                "production_id": f"PROD-{i:06d}-{location['location_id']}",
                "sku_id": sku["sku_id"],
                "location_id": location["location_id"],
                "planned_quantity": planned_quantity,
                "production_capacity": production_capacity,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "status": "Planned"
            })

    return records


# Generate master data
if __name__ == "__main__":
    skus = generate_skus()
    locations = generate_locations()
    suppliers = generate_suppliers()


    demand = generate_forecast_demand(skus, locations)
    inventory = generate_inventory(skus, locations)
    capacity = generate_supplier_capacity(skus, suppliers)
    lead_times = generate_lead_times(skus, suppliers)

    # Generate purchase orders
    purchase_orders = generate_purchase_orders(
        skus, locations, suppliers, capacity, lead_times
    )

    # Generate production plans
    production_plans = generate_production_plans(
        skus, locations
    )

    # Save master data
    save_csv(MASTER_FOLDER, "skus.csv", skus)
    save_csv(MASTER_FOLDER, "locations.csv", locations)
    save_csv(MASTER_FOLDER, "suppliers.csv", suppliers)

    # Save dependent data
    save_csv(TRANSACTION_FOLDER, "forecast_demand.csv", demand)
    save_csv(TRANSACTION_FOLDER, "inventory.csv", inventory)
    save_csv(TRANSACTION_FOLDER, "supplier_capacity.csv", capacity)
    save_csv(TRANSACTION_FOLDER, "lead_times.csv", lead_times)

    # Save transaction data
    save_csv(TRANSACTION_FOLDER, "purchase_orders.csv", purchase_orders)
    save_csv(TRANSACTION_FOLDER, "production_plans.csv", production_plans)

    # Display record counts
    print("\nALL DATA GENERATION COMPLETED")
    print("SKU:", len(skus))
    print("Locations:", len(locations))
    print("Suppliers:", len(suppliers))
    print("Forecast Demand:", len(demand))
    print("Inventory:", len(inventory))
    print("Supplier Capacity:", len(capacity))
    print("Lead Times:", len(lead_times))
    print("Purchase Orders:", len(purchase_orders))
    print("Production Plans:", len(production_plans))

    skus = generate_skus()
    locations = generate_locations()
    suppliers = generate_suppliers()

    demand = generate_forecast_demand(skus, locations)
    inventory = generate_inventory(skus, locations)
    capacity = generate_supplier_capacity(skus, suppliers)
    lead_times = generate_lead_times(skus, suppliers)


    purchase_orders = generate_purchase_orders(
            skus, locations, suppliers, capacity, lead_times
    )

    production_plans = generate_production_plans(skus, locations)

    save_csv(MASTER_FOLDER, "skus.csv", skus)
    save_csv(MASTER_FOLDER, "locations.csv", locations)
    save_csv(MASTER_FOLDER, "suppliers.csv", suppliers)

    save_csv(TRANSACTION_FOLDER, "forecast_demand.csv", demand)
    save_csv(TRANSACTION_FOLDER, "inventory.csv", inventory)
    save_csv(TRANSACTION_FOLDER, "supplier_capacity.csv", capacity)
    save_csv(TRANSACTION_FOLDER, "lead_times.csv", lead_times)

    save_csv(TRANSACTION_FOLDER, "purchase_orders.csv", purchase_orders)

    save_csv(TRANSACTION_FOLDER, "production_plans.csv", production_plans)

    print("\nDEPENDENT DATA GENERATION COMPLETED")
    print("SKU records:", len(skus))
    print("Location records:", len(locations))
    print("Supplier records:", len(suppliers))
    print("Forecast demand records:", len(demand))
    print("Inventory records:", len(inventory))
    print("Supplier capacity records:", len(capacity))
    print("Lead time records:", len(lead_times))

    print("Purchase order records:", len(purchase_orders))
    print("Production plan records:", len(production_plans))