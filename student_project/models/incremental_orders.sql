{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select
    order_id,
    customer_id,
    total_price,
    order_date
from {{ ref('new_orders') }}

union all

select
    o_orderkey as order_id,
    o_custkey as customer_id,
    o_totalprice as total_price,
    o_orderdate as order_date
from {{ source('tpch', 'orders') }}

{% if is_incremental() %}
    where o_orderdate > (select max(order_date) from {{ this }})
{% endif %}