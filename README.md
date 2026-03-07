# dbt + Databricks Analytics Project

This project demonstrates how **dbt can be used with Databricks** to implement a modular analytics engineering workflow.  
The pipeline transforms **TPCH sample data available in Databricks** into analytics-ready models using dbt transformations, data quality tests, and documentation.

---

## Architecture

Databricks Sample Data  
↓  
Staging Layer (data cleaning and standardization)  
↓  
Mart Layer (business-level aggregations)

---

## Project Structure

```
models/
  staging/
    staging_orders.sql
    schema.yml

  marts/
    fct_customer_revenue.sql

  example/
    default dbt example models

dbt_project.yml
README.md
```

---

## Key Concepts Demonstrated

### dbt Models
SQL models were created to transform raw TPCH order data into analytics-ready datasets.

### Layered Data Modeling
The project follows a common analytics engineering pattern:

- **Staging Layer** – standardizes and cleans raw source data
- **Mart Layer** – creates business-level aggregations for analytics

### Dependency Management
dbt’s `ref()` function is used to define dependencies between models.  
This allows dbt to automatically build a **Directed Acyclic Graph (DAG)** and execute transformations in the correct order.

Example:

```sql
select *
from {{ ref('staging_orders') }}
```

### Data Quality Testing
dbt tests were implemented to enforce data quality checks.

Example tests include:

- `unique`
- `not_null`

Tests can be executed using:

```
dbt test
```

### Documentation and Lineage
dbt documentation was generated using:

```
dbt docs generate
dbt docs serve
```

This provides an interactive interface showing:

- model lineage
- column metadata
- applied tests
- model dependencies

---

## Technologies Used

- **dbt**
- **Databricks**
- **SQL**
- **Python (virtual environment)**

---

## What This Project Demonstrates

- Connecting dbt to Databricks
- Implementing modular SQL transformations
- Managing model dependencies with `ref()`
- Applying automated data quality tests
- Generating documentation and lineage for data pipelines

---

## Possible Future Enhancements

- Implement incremental models for large datasets
- Define dbt sources for raw data
- Add seed data for reference tables
- Implement snapshot models for change tracking
