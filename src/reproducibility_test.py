
import hashlib
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILES = [
    "data/master/skus.csv",
    "data/master/locations.csv",
    "data/master/suppliers.csv",
    "data/transactions/forecast_demand.csv",
    "data/transactions/inventory.csv",
    "data/transactions/supplier_capacity.csv",
    "data/transactions/lead_times.csv",
    "data/transactions/purchase_orders.csv",
    "data/transactions/production_plans.csv"
]

def calculate_checksum(file_path):
    content = file_path.read_bytes()
    return hashlib.sha256(content).hexdigest()

def get_checksums():
    results = {}

    for filename in FILES:
        path = PROJECT_ROOT / filename

        if not path.exists():
            raise FileNotFoundError(filename)

        results[filename] = calculate_checksum(path)

    return results


print("REPRODUCIBILITY TEST STARTED")

# First generation
subprocess.run(
    [sys.executable, "src/data_generation.py"],
    cwd=PROJECT_ROOT,
    check=True
)

first_run = get_checksums()

# Second generation using the same seed
subprocess.run(
    [sys.executable, "src/data_generation.py"],
    cwd=PROJECT_ROOT,
    check=True
)

second_run = get_checksums()

# Compare both generations
print("\nREPRODUCIBILITY RESULTS")

all_match = True

for filename in FILES:
    match = first_run[filename] == second_run[filename]

    print(filename, ":", "MATCH" if match else "MISMATCH")

    if not match:
        all_match = False

if all_match:
    print("\nPASS: Both runs produced identical files.")
else:
    print("\nFAIL: Generated files are different.")
