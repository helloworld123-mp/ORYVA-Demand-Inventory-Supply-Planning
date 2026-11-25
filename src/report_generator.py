
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "ground_truth"
REPORT_FOLDER = PROJECT_ROOT / "reports"

REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

# Load planning results
pab = pd.read_csv(DATA_FOLDER / "pab_results.csv")
shortages = pd.read_csv(DATA_FOLDER / "shortages.csv")

# 1. Shortage count by SKU
shortage_by_sku = (
    shortages.groupby("sku_id")["shortage_quantity"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 5))
shortage_by_sku.plot(kind="bar")
plt.title("Total Shortage Quantity by SKU")
plt.xlabel("SKU")
plt.ylabel("Shortage Quantity")
plt.tight_layout()
plt.savefig(REPORT_FOLDER / "shortage_by_sku.png")
plt.close()

# 2. Weekly demand and available inventory
weekly = (
    pab.groupby("week")[["forecast_demand", "opening_stock"]]
    .sum()
)

plt.figure(figsize=(12, 5))
weekly.plot()
plt.title("Weekly Forecast Demand and Opening Stock")
plt.xlabel("Week")
plt.ylabel("Quantity")
plt.tight_layout()
plt.savefig(REPORT_FOLDER / "weekly_inventory.png")
plt.close()

# 3. Summary report
summary = pd.DataFrame({
    "Metric": [
        "Total PAB Records",
        "Total Shortage Records",
        "Total Shortage Quantity",
        "Average Forecast Demand"
    ],
    "Value": [
        len(pab),
        len(shortages),
        shortages["shortage_quantity"].sum(),
        pab["forecast_demand"].mean()
    ]
})

summary.to_csv(REPORT_FOLDER / "planning_summary.csv", index=False)

print("REPORT GENERATION COMPLETED")
print("PAB Records:", len(pab))
print("Shortage Records:", len(shortages))
print("Reports saved in:", REPORT_FOLDER)
