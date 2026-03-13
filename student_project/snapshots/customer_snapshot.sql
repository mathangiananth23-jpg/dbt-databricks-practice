{% snapshot customer_snapshot %}

{{
    config(
        target_schema='default',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'address', 'nation_key']
    )
}}

select * from {{ ref('customers') }}

{% endsnapshot %}