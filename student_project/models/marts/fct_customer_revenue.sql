select
    customer_id,
    count(order_id) as total_orders,
    sum(total_price) as total_revenue
from {{ ref('staging_orders') }}
group by customer_id