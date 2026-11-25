
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

scripts = [
    "src/data_generation.py",
    "src/planning_engine.py",
    "src/validate_planning.py",
    "src/edge_case_generator.py",
    "src/edge_case_validator.py",
    "src/reproducibility_test.py",
    "src/report_generator.py"
]

print("=" * 50)
print("ORYVA AI - DEMAND, INVENTORY & SUPPLY PLANNING")
print("=" * 50)

for script in scripts:
    script_path = PROJECT_ROOT / script

    print(f"\nRunning: {script}")

    if not script_path.exists():
        print(f"ERROR: File not found: {script}")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print(f"\nERROR: {script} failed.")
        sys.exit(result.returncode)

print("\n" + "=" * 50)
print("PROJECT EXECUTION COMPLETED")
print("=" * 50)
