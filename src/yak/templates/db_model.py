import sqlalchemy as sa

from sqlalchemy.dialects import {% if database == 'aiomysql' -%}
mysql
{%- elif database == 'aiopg' -%}
postgresql
{%- endif %} as dialect

from {{ project_name }}.db import meta


address_tbl = sa.Table(
    '{{ table_name }}', meta,
    {% for column in columns %}sa.Column({{ column['string'] }}),
    {% endfor -%}
)
