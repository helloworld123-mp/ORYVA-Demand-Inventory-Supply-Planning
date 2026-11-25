
import pandas as pd
from pathlib import Path

# 1. Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MASTER_FOLDER = PROJECT_ROOT / "data" / "master"
TRANSACTION_FOLDER = PROJECT_ROOT / "data" / "transactions"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "ground_truth"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# 2. Load generated data
def load_data():

    skus = pd.read_csv(MASTER_FOLDER / "skus.csv")
    locations = pd.read_csv(MASTER_FOLDER / "locations.csv")

    demand = pd.read_csv(TRANSACTION_FOLDER / "forecast_demand.csv")
    inventory = pd.read_csv(TRANSACTION_FOLDER / "inventory.csv")

    purchase_orders = pd.read_csv(
        TRANSACTION_FOLDER / "purchase_orders.csv"
    )

    production = pd.read_csv(
        TRANSACTION_FOLDER / "production_plans.csv"
    )

    return skus, locations, demand, inventory, purchase_orders, production


# 3. Calculate weekly PAB and shortages
def calculate_planning(demand, inventory, purchase_orders, production):

    results = []
    shortages = []

    for _, stock in inventory.iterrows():

        sku_id = stock["sku_id"]
        location_id = stock["location_id"]

        opening_stock = float(stock["on_hand_quantity"])

        sku_demand = demand[
            (demand["sku_id"] == sku_id) &
            (demand["location_id"] == location_id)
        ].sort_values("week")

        for _, week_data in sku_demand.iterrows():

            week = week_data["week"]
            forecast = float(week_data["forecast_quantity"])

            week_number = int(week[-2:])

            receipts = 0
            production_quantity = 0

            # Count purchase orders arriving in this week
            for _, po in purchase_orders.iterrows():

                if (po["sku_id"] == sku_id and
                    po["location_id"] == location_id):

                    delivery_date = pd.to_datetime(
                        po["expected_delivery_date"]
                    )

                    if delivery_date.isocalendar().week == week_number:
                        receipts += float(po["order_quantity"])

            # Count planned production in this week
            for _, plan in production.iterrows():

                if (plan["sku_id"] == sku_id and
                    plan["location_id"] == location_id):

                    production_date = pd.to_datetime(plan["end_date"])

                    if production_date.isocalendar().week == week_number:
                        production_quantity += float(plan["planned_quantity"])

            available = (
                opening_stock +
                receipts +
                production_quantity
            )

            pab = available - forecast

            shortage_quantity = max(0, -pab)

            results.append({
                "sku_id": sku_id,
                "location_id": location_id,
                "week": week,
                "opening_stock": opening_stock,
                "receipts": receipts,
                "production_quantity": production_quantity,
                "forecast_demand": forecast,
                "projected_available_balance": pab
            })

            if shortage_quantity > 0:

                shortages.append({
                    "shortage_id": f"SHORT-2026-{len(shortages)+1:06d}",
                    "sku_id": sku_id,
                    "location_id": location_id,
                    "week": week,
                    "required_quantity": forecast,
                    "available_quantity": available,
                    "shortage_quantity": shortage_quantity,
                    "cause": "Insufficient projected inventory",
                    "status": "Open"
                })

            # Carry closing balance into the next week
            opening_stock = max(0, pab)

    return results, shortages


# 4. Generate mitigation options
def generate_mitigations(shortages):

    mitigations = []

    for shortage in shortages:

        mitigations.append({
            "mitigation_id": f"MIT-{shortage['shortage_id']}-01",
            "shortage_id": shortage["shortage_id"],
            "option_type": "Additional Procurement",
            "proposed_quantity": shortage["shortage_quantity"],
            "estimated_cost": 0,
            "expected_arrival_date": "",
            "feasibility_status": "Requires Supplier Validation",
            "service_impact": "May reduce shortage",
            "recommendation_reason": "Additional supply is required"
        })

    return mitigations


# 5. Run planning engine
if __name__ == "__main__":

    print("Loading generated data...")

    skus, locations, demand, inventory, purchase_orders, production = load_data()

    print("Calculating weekly inventory balances...")

    pab_results, shortages = calculate_planning(
        demand, inventory, purchase_orders, production
    )

    mitigations = generate_mitigations(shortages)

    # 6. Export results
    pd.DataFrame(pab_results).to_csv(
        OUTPUT_FOLDER / "pab_results.csv", index=False
    )

    pd.DataFrame(shortages).to_csv(
        OUTPUT_FOLDER / "shortages.csv", index=False
    )

    pd.DataFrame(mitigations).to_csv(
        OUTPUT_FOLDER / "mitigation_options.csv", index=False
    )

    print("\nPLANNING ENGINE COMPLETED")
    print("PAB Records:", len(pab_results))
    print("Shortages:", len(shortages))
    print("Mitigation Options:", len(mitigations))
    print("Output folder:", OUTPUT_FOLDER)
