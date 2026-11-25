
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data" / "ground_truth"

# Load edge cases
edge_cases = pd.read_csv(DATA_FOLDER / "edge_cases.csv")

# Load supplier and planning data
capacity = pd.read_csv(
    PROJECT_ROOT / "data" / "transactions" / "supplier_capacity.csv"
)

lead_times = pd.read_csv(
    PROJECT_ROOT / "data" / "transactions" / "lead_times.csv"
)

print("\nEDGE CASE VALIDATION")
print("--------------------")

for _, case in edge_cases.iterrows():

    issue = case["issue_type"]

    if issue == "Duplicate Inbound":
        result = "SCENARIO DEFINED - Duplicate detection required"

    elif issue == "Unapproved Substitute SKU":
        result = "SCENARIO DEFINED - Substitution approval required"

    elif issue == "Supplier Capacity Exceeded":
        result = "CAPACITY DATA AVAILABLE - Violation test required"

    elif issue == "Missing Lead Time":
        result = "LEAD TIME DATA AVAILABLE - Missing record test required"

    elif issue == "UOM Mismatch":
        result = "SCENARIO DEFINED - Unit validation required"

    else:
        result = "UNKNOWN SCENARIO"

    print(case["issue_id"], "-", issue)
    print(result)

print("\nTOTAL SCENARIOS:", len(edge_cases))
print("EDGE CASE REVIEW COMPLETED")
