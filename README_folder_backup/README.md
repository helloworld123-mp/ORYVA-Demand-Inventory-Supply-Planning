# ORYVA AI – Demand, Inventory & Supply Planning

## 1. Project Overview

This project demonstrates a Demand, Inventory and Supply Planning solution.

The system uses forecast demand, inventory levels, supplier information, purchase orders, lead times and production plans to calculate projected inventory availability and identify potential shortages.

It also generates mitigation options and planning reports to support supply planning decisions.

## 2. Project Objectives

- Generate and manage synthetic supply chain data.
- Calculate projected available balance (PAB).
- Identify potential inventory shortages.
- Generate mitigation option records.
- Define and review important supply chain edge cases.
- Validate planning data.
- Test reproducibility using a fixed random seed.
- Generate reports for planning analysis.

## 3. Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- CSV files
- Visual Studio Code
- Git and GitHub

## 4. Project Structure

```text
ORYVA_Demand_Inventory_Planning/
│
├── data/
│   ├── master/
│   ├── transactions/
│   └── ground_truth/
│
├── src/
│   ├── data_generation.py
│   ├── planning_engine.py
│   ├── validate_planning.py
│   ├── edge_case_generator.py
│   ├── edge_case_validator.py
│   ├── reproducibility_test.py
│   └── report_generator.py
│
├── docs/
│   ├── data_dictionary.md
│   └── schema.md
│
├── reports/
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

## 5. Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## 6. Data Generation

The project uses synthetic data generated with a fixed random seed.

The current starter configuration uses:

- 10 SKUs
- 3 locations
- 10 suppliers
- 52 weeks of forecast demand

Random seed: `20261022`

Run the data generator:

```bash
python src/data_generation.py
```

Generated data is stored in the `data/` directory.

## 7. Planning Engine

Run the planning engine:

```bash
python src/planning_engine.py
```

The planning engine generates:

- Projected Available Balance (PAB)
- Shortage records
- Mitigation option records

Output files are stored in `data/ground_truth/`.

## 8. Data Validation

Run the validation script:

```bash
python src/validate_planning.py
```

The script performs the implemented planning-data validation checks.

## 9. Edge Case Scenarios

The project defines five important supply chain edge cases:

1. Duplicate inbound inventory
2. Unapproved substitute SKU
3. Supplier capacity exceeded
4. Missing lead time
5. Unit of measurement mismatch

Generate the edge case scenario definitions:

```bash
python src/edge_case_generator.py
```

Review the generated scenarios:

```bash
python src/edge_case_validator.py
```

## 10. Reproducibility Testing

Run:

```bash
python src/reproducibility_test.py
```

The reproducibility test runs the data generator twice with the same random seed and compares the generated input CSV files using SHA-256 checksums.

## 11. Report Generation

Run:

```bash
python src/report_generator.py
```

The generated reports include:

- Shortage by SKU chart
- Weekly inventory chart
- Planning summary CSV

Reports are saved in the `reports/` directory.

## 12. Documentation

The `docs/` directory contains:

- `data_dictionary.md` – Entity definitions, fields and data descriptions.
- `schema.md` – Primary keys, foreign keys, relationships, constraints, lifecycle states and event history.

## 13. Data Source

This project uses synthetically generated data for demonstration and testing.

The data is generated using a fixed random seed to support repeatable generation.

No real company or customer data is required for the current starter dataset.

## 14. Current Implementation Scope

The current implementation includes data generation, planning calculations, shortage and mitigation output generation, scenario definitions, validation scripts, reproducibility testing and report generation.

The edge case scenarios are currently defined for review. Full automated detection of each scenario and comprehensive validation of all supply planning rules require further implementation and testing.