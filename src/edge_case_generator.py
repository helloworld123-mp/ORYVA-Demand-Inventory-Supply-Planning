
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "ground_truth"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Five controlled edge cases
edge_cases = [
    {
        "issue_id": "EDGE-001",
        "issue_type": "Duplicate Inbound",
        "description": "The same inbound purchase order is counted twice.",
        "ground_truth": "INVALID",
        "expected_result": "Duplicate supply must be detected."
    },
    {
        "issue_id": "EDGE-002",
        "issue_type": "Unapproved Substitute SKU",
        "description": "An unapproved substitute SKU is used to satisfy demand.",
        "ground_truth": "INVALID",
        "expected_result": "Unapproved substitution must be rejected."
    },
    {
        "issue_id": "EDGE-003",
        "issue_type": "Supplier Capacity Exceeded",
        "description": "The purchase order quantity exceeds supplier capacity.",
        "ground_truth": "INVALID",
        "expected_result": "Capacity violation must be detected."
    },
    {
        "issue_id": "EDGE-004",
        "issue_type": "Missing Lead Time",
        "description": "Supply is considered without valid lead-time information.",
        "ground_truth": "INVALID",
        "expected_result": "Supply timing must be flagged as uncertain."
    },
    {
        "issue_id": "EDGE-005",
        "issue_type": "UOM Mismatch",
        "description": "Demand and inventory use incompatible units.",
        "ground_truth": "INVALID",
        "expected_result": "Unit conversion or validation is required."
    }
]

# Export edge cases separately
df = pd.DataFrame(edge_cases)

df.to_csv(
    OUTPUT_FOLDER / "edge_cases.csv",
    index=False
)

print("EDGE CASE GENERATION COMPLETED")
print("Total edge cases:", len(df))
print("Output:", OUTPUT_FOLDER / "edge_cases.csv")
