dbt + Databricks Analytics Project
This project demonstrates how dbt can be used with Databricks to implement a modular analytics engineering workflow.
The pipeline transforms TPCH sample data available in Databricks into analytics-ready models using dbt transformations, data quality tests, and documentation.

Architecture
Databricks Sample Data (samples.tpch)
↓
Sources Layer (sources.yml — defines raw data connections)
↓
Staging Layer (data cleaning and standardization)
↓
Mart Layer (business-level aggregations)
↓
Snapshots (SCD Type 2 historical tracking)

Project Structure
student_project/
├── models/
│   ├── staging/
│   │   ├── staging_orders.sql
│   │   └── sources.yml
│   ├── marts/
│   │   └── fct_customer_revenue.sql
│   └── incremental_orders.sql
├── snapshots/
│   └── customer_snapshot.sql
├── seeds/
│   ├── customers.csv
│   └── new_orders.csv
├── tests/
├── macros/
├── dbt_project.yml
└── README.md

Key Concepts Demonstrated
Sources
Raw data connections are defined in sources.yml using the {{ source() }} function.
This decouples raw table references from transformation logic — if a table name changes, it is updated in one place only.
yamlsources:
  - name: tpch
    database: samples
    schema: tpch
    tables:
      - name: orders
      - name: customer
Layered Data Modeling
The project follows the standard analytics engineering pattern:

Staging Layer — standardizes and cleans raw source data
Mart Layer — creates business-level aggregations for analytics

Incremental Models
An incremental model processes only new or updated rows on each run instead of rebuilding the entire table — making it efficient for large datasets.
sql{{ config(materialized='incremental', unique_key='order_id') }}

select ...
from {{ source('tpch', 'orders') }}

{% if is_incremental() %}
    where o_orderdate > (select max(order_date) from {{ this }})
{% endif %}
Snapshots — SCD Type 2
Snapshot models track historical changes to dimension data using Slowly Changing Dimension Type 2 methodology.
When a record changes, dbt closes the old version by setting dbt_valid_to and inserts a new row with dbt_valid_to = null.
sql{% snapshot customer_snapshot %}
{{
    config(
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'address', 'nation_key']
    )
}}
select * from {{ ref('customers') }}
{% endsnapshot %}
Seeds
Static reference data is loaded into Databricks using dbt seeds — CSV files that are version controlled alongside the project code.
bashdbt seed
Dependency Management
dbt's ref() function defines dependencies between models, allowing dbt to automatically build a Directed Acyclic Graph (DAG) and execute transformations in the correct order.
Data Quality Testing
dbt tests enforce data quality checks across models.
Tests implemented:

unique
not_null

bashdbt test
Documentation and Lineage
dbt documentation was generated using:
bashdbt docs generate
dbt docs serve
This provides an interactive interface showing model lineage, column metadata, applied tests, and model dependencies.

Technologies Used

dbt Core 1.11
Databricks (Community Edition)
Apache Spark SQL
Python (virtual environment)


What This Project Demonstrates

Connecting dbt to Databricks using profiles.yml
Defining sources and referencing raw data with {{ source() }}
Implementing modular SQL transformations across staging and mart layers
Building incremental models for efficient data processing
Implementing SCD Type 2 historical tracking using dbt snapshots
Loading reference data using dbt seeds
Managing model dependencies with ref()
Applying automated data quality tests
Generating documentation and lineage for data pipelines
