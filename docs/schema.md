
# DATABASE SCHEMA
## ORYVA AI – Demand, Inventory & Supply Planning

## 1. Primary Keys and Foreign Keys

| Entity | Primary Key (PK) | Foreign Keys (FK) |
|---|---|---|
| SKU | sku_id | None |
| Location | location_id | None |
| ForecastDemand | demand_id | sku_id, location_id |
| Inventory | inventory_id | sku_id, location_id |
| Supplier | supplier_id | None |
| SupplierCapacity | capacity_id | supplier_id, sku_id |
| LeadTime | lead_time_id | supplier_id, sku_id |
| PurchaseOrder | po_id | supplier_id, sku_id, location_id |
| ProductionPlan | production_id | sku_id, location_id |
| Shortage | shortage_id | sku_id, location_id |
| MitigationOption | mitigation_id | shortage_id |

## 2. Relationship Cardinality

| Parent Entity | Child Entity | Relationship | Explanation |
|---|---|---|---|
| SKU | ForecastDemand | 1:N | One SKU can have multiple demand records |
| Location | ForecastDemand | 1:N | One location can have multiple demand records |
| SKU | Inventory | 1:N | One SKU can have multiple inventory records |
| Location | Inventory | 1:N | One location can store multiple inventory records |
| Supplier | SupplierCapacity | 1:N | One supplier can have multiple capacity records |
| SKU | SupplierCapacity | 1:N | One SKU can have multiple supplier capacity records |
| Supplier | LeadTime | 1:N | One supplier can have multiple lead-time records |
| SKU | LeadTime | 1:N | One SKU can have multiple lead-time records |
| Supplier | PurchaseOrder | 1:N | One supplier can receive multiple purchase orders |
| SKU | PurchaseOrder | 1:N | One SKU can appear in multiple purchase orders |
| Location | PurchaseOrder | 1:N | One location can receive multiple purchase orders |
| SKU | ProductionPlan | 1:N | One SKU can have multiple production plans |
| Location | ProductionPlan | 1:N | One location can have multiple production plans |
| SKU | Shortage | 1:N | One SKU can have multiple shortages |
| Location | Shortage | 1:N | One location can have multiple shortages |
| Shortage | MitigationOption | 1:N | One shortage can have multiple mitigation options |

## 3. Many-to-Many Relationships

Supplier and SKU have a many-to-many relationship.

- One supplier can supply multiple SKUs.
- One SKU can be supplied by multiple suppliers.

To manage this relationship, SupplierCapacity acts as a bridge table.

It connects:
- supplier_id
- sku_id

Each supplier-SKU combination can have its own capacity and minimum order quantity.

## 4. Optional Relationships

1. Supplier contact_email is optional.
2. SupplierCapacity effective_to is optional.
3. LeadTime effective_to is optional.
4. MitigationOption expected_arrival_date is optional.
5. A shortage may initially have no mitigation options.
6. A production plan may be optional when a product is sourced externally.

## 5. Effective Dates

SupplierCapacity and LeadTime records must maintain effective dates.

Rules:
- effective_from is mandatory.
- effective_to is optional.
- effective_to must not precede effective_from.
- Only applicable records should be used during planning.
- Historical records must be preserved when values change.

## 6. Lifecycle States

### PurchaseOrder
Draft → Placed → In Transit → Received

A purchase order may also be Cancelled.

### ProductionPlan
Planned → In Progress → Completed

A production plan may also be Cancelled.

### Shortage
Open → Under Review → Resolved

### MitigationOption
Pending → Feasible / Not Feasible

Invalid state transitions must be rejected.

## 7. Data Integrity Rules

1. All primary keys must be unique.
2. Every foreign key must reference an existing parent record.
3. Duplicate supplier-SKU capacity records for the same effective period must be prevented.
4. Duplicate weekly demand for the same SKU and location must be prevented.
5. Historical records must not be overwritten.
6. All relationships must be validated before planning calculations.
7. All state changes must be recorded.



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



## 9. Event History and Traceability

The system must maintain a history of important changes made to business records.

### EntityEvent

A supporting event history table will be maintained with the following fields:

| Field | Description |
|---|---|
| event_id | Unique identifier for each event |
| entity_type | Type of entity being updated |
| entity_id | ID of the affected record |
| previous_state | Previous status or value |
| new_state | Updated status or value |
| event_type | Type of change or action |
| event_timestamp | Date and time of the event |
| reason | Explanation for the change |

### Event History Rules

1. Every important state change must create a new event record.
2. Previous event records must never be overwritten or deleted.
3. Each event must have a unique event_id.
4. Each event must identify the affected entity and record.
5. Event timestamps must be recorded.
6. Changes must be validated against the allowed lifecycle transitions.
7. The application must verify that entity_type and entity_id refer to an existing record.

EntityEvent is a supporting audit table and does not replace the 11 core business entities.
