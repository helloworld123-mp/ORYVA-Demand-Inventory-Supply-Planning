# DATA DICTIONARY
## Demand, Inventory & Supply Planning
### ORYVA AI Technical Assignment

## 1. SKU (Product Information)

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| sku_id | String | Yes | SKU-000001 format | N/A | Yes | Must be unique |
| product_name | String | Yes | Any valid name | N/A | No | Cannot be empty |
| category | String | Yes | Electronics, Clothing, Food, Other | N/A | No | Must be a valid category |
| unit | String | Yes | Pieces, Boxes, Kg, Litres | N/A | No | Must be an approved unit |
| status | String | Yes | Active, Inactive | N/A | No | Must match allowed values |

## 2. Location

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| location_id | String | Yes | LOC-000001 format | N/A | Yes | Must be unique |
| location_name | String | Yes | Valid location name | N/A | No | Cannot be empty |
| city | String | Yes | Valid city name | N/A | No | Cannot be empty |
| state | String | Yes | Valid state name | N/A | No | Cannot be empty |
| status | String | Yes | Active, Inactive | N/A | No | Must match allowed values |


## 3. ForecastDemand

Stores expected customer demand for a particular product, location and week.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| demand_id | String | Yes | DEM-<sku>-<location>-2026W01 | N/A | Yes | Must follow ID convention |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| location_id | String | Yes | Existing Location ID | N/A | No | Must reference Location |
| week | String | Yes | 2026W01 to 2026W52 | Week | No | Must be a valid week |
| forecast_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| created_date | Date | Yes | YYYY-MM-DD | Date | No | Must be a valid date |

**Additional Rule:** The combination of sku_id, location_id and week must be unique.


## 4. Inventory

Stores available product stock at each location.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| inventory_id | String | Yes | INV-000001 format | N/A | Yes | Must be unique |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| location_id | String | Yes | Existing Location ID | N/A | No | Must reference Location |
| on_hand_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| inbound_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| as_of_date | Date | Yes | YYYY-MM-DD | Date | No | Must be a valid date |


## 5. Supplier

Stores information about companies supplying products.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| supplier_id | String | Yes | SUP-000001 format | N/A | Yes | Must be unique |
| supplier_name | String | Yes | Valid company name | N/A | No | Cannot be empty |
| contact_email | String | No | Valid email format | N/A | No | Must be valid if provided |
| status | String | Yes | Active, Inactive | N/A | No | Must match allowed values |


## 6. SupplierCapacity

Stores the maximum and minimum supply quantities of suppliers.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| capacity_id | String | Yes | CAP-000001 format | N/A | Yes | Must be unique |
| supplier_id | String | Yes | Existing Supplier ID | N/A | No | Must reference Supplier |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| max_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| min_order_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot exceed max_quantity |
| effective_from | Date | Yes | YYYY-MM-DD | Date | No | Must be valid |
| effective_to | Date | No | YYYY-MM-DD | Date | No | Must be after effective_from |


## 7. LeadTime

Stores the time required by a supplier to deliver products.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| lead_time_id | String | Yes | LT-000001 format | N/A | Yes | Must be unique |
| supplier_id | String | Yes | Existing Supplier ID | N/A | No | Must reference Supplier |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| lead_time_days | Integer | Yes | 0 or greater | Days | No | Cannot be negative |
| effective_from | Date | Yes | YYYY-MM-DD | Date | No | Must be valid |
| effective_to | Date | No | YYYY-MM-DD | Date | No | Must be after effective_from |


## 8. PurchaseOrder

Stores orders placed with suppliers.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| po_id | String | Yes | PO-2026-000001 format | N/A | Yes | Must follow ID convention |
| supplier_id | String | Yes | Existing Supplier ID | N/A | No | Must reference Supplier |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| location_id | String | Yes | Existing Location ID | N/A | No | Must reference Location |
| order_quantity | Integer | Yes | Greater than 0 | Product unit | No | Must be positive |
| order_date | Date | Yes | YYYY-MM-DD | Date | No | Must be valid |
| expected_delivery_date | Date | Yes | YYYY-MM-DD | Date | No | Cannot be before order date |
| received_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot exceed order quantity |
| status | String | Yes | Draft, Placed, In Transit, Received, Cancelled | N/A | No | Must match allowed values |


## 9. ProductionPlan

Stores planned product manufacturing details.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| production_id | String | Yes | PROD-000001 format | N/A | Yes | Must be unique |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| location_id | String | Yes | Existing Location ID | N/A | No | Must reference Location |
| planned_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| production_capacity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| start_date | Date | Yes | YYYY-MM-DD | Date | No | Must be valid |
| end_date | Date | Yes | YYYY-MM-DD | Date | No | Must not precede start date |
| status | String | Yes | Planned, In Progress, Completed, Cancelled | N/A | No | Must match allowed values |


## 10. Shortage

Stores detected inventory shortages.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| shortage_id | String | Yes | SHORT-2026-000001 format | N/A | Yes | Must follow ID convention |
| sku_id | String | Yes | Existing SKU ID | N/A | No | Must reference SKU |
| location_id | String | Yes | Existing Location ID | N/A | No | Must reference Location |
| week | String | Yes | Valid year and week | Week | No | Must be valid |
| required_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| available_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| shortage_quantity | Integer | Yes | Greater than 0 | Product unit | No | Must equal unmet demand |
| cause | String | Yes | Insufficient stock, Delayed delivery, Capacity constraint, Other | N/A | No | Must have an explainable cause |
| status | String | Yes | Open, Under Review, Resolved | N/A | No | Must match allowed values |


## 11. MitigationOption

Stores possible solutions for detected shortages.

| Field Name | Data Type | Required | Allowed Values | Unit | Unique | Validation Rule |
|---|---|---|---|---|---|---|
| mitigation_id | String | Yes | MIT-<shortage-id>-01 | N/A | Yes | Must follow ID convention |
| shortage_id | String | Yes | Existing Shortage ID | N/A | No | Must reference Shortage |
| option_type | String | Yes | Alternate Supplier, Stock Transfer, Production, Reschedule | N/A | No | Must match allowed values |
| proposed_quantity | Integer | Yes | 0 or greater | Product unit | No | Cannot be negative |
| estimated_cost | Decimal | Yes | 0 or greater | INR | No | Cannot be negative |
| expected_arrival_date | Date | No | YYYY-MM-DD | Date | No | Must be valid if provided |
| feasibility_status | String | Yes | Feasible, Not Feasible, Pending | N/A | No | Must match allowed values |
| service_impact | String | Yes | Low, Medium, High | N/A | No | Must match allowed values |
| recommendation_reason | String | Yes | Explanation | N/A | No | Cannot be empty |



# 12. Common Data Validation Rules

1. Every primary key must be unique.
2. All foreign keys must reference existing records.
3. IDs must follow the prescribed naming conventions.
4. IDs must remain immutable after creation.
5. Required fields cannot contain NULL or empty values.
6. Quantities must not be negative.
7. Dates must follow YYYY-MM-DD format.
8. Effective end dates must not precede effective start dates.
9. Product quantities must use consistent units of measurement.
10. Derived values must be calculated from source records.
11. Duplicate records must be detected.
12. All state changes must preserve event history.

# 13. Data Dictionary Notes

- All records must have valid primary keys.
- Related records must maintain foreign-key integrity.
- Optional fields may contain NULL values.
- All date and quantity validations must be performed before processing.
- The data dictionary will be used as the reference for synthetic data generation and validation.



## 8. Entity Relationship Diagram

The following diagram represents the relationships between all major entities in the planning system.

~~~mermaid
erDiagram
    SKU ||--o{ ForecastDemand : has
    LOCATION ||--o{ ForecastDemand : receives

    SKU ||--o{ INVENTORY : stored_as
    LOCATION ||--o{ INVENTORY : stores

    SUPPLIER ||--o{ SUPPLIERCAPACITY : provides
    SKU ||--o{ SUPPLIERCAPACITY : supplied_as

    SUPPLIER ||--o{ LEADTIME : has
    SKU ||--o{ LEADTIME : delivered_as

    SUPPLIER ||--o{ PURCHASEORDER : receives
    SKU ||--o{ PURCHASEORDER : ordered
    LOCATION ||--o{ PURCHASEORDER : delivered_to

    SKU ||--o{ PRODUCTIONPLAN : manufactured
    LOCATION ||--o{ PRODUCTIONPLAN : planned_at

    SKU ||--o{ SHORTAGE : experiences
    LOCATION ||--o{ SHORTAGE : occurs_at

    SHORTAGE ||--o{ MITIGATIONOPTION : resolved_by
~~~
