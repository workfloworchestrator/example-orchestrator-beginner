"""add user and usergroup products.

Revision ID: 9a31b6bf3e85
Revises:
Create Date: 2023-10-03 22:25:10.190209

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9a31b6bf3e85'
down_revision = None
branch_labels = ('data',)
depends_on = 'da5c9f4cce1c'


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
INSERT INTO products (name, description, product_type, tag, status) VALUES ('User Group', 'user group administration', 'UserGroup', 'GROUP', 'active') RETURNING products.product_id
    """))
    conn.execute(sa.text("""
INSERT INTO products (name, description, product_type, tag, status) VALUES ('User internal', 'user administration - internal', 'User', 'USER_INT', 'active') RETURNING products.product_id
    """))
    conn.execute(sa.text("""
INSERT INTO products (name, description, product_type, tag, status) VALUES ('User external', 'user administration - external', 'User', 'USER_EXT', 'active') RETURNING products.product_id
    """))
    conn.execute(sa.text("""
INSERT INTO fixed_inputs (name, value, product_id) VALUES ('affiliation', 'internal', (SELECT products.product_id FROM products WHERE products.name IN ('User internal'))), ('affiliation', 'external', (SELECT products.product_id FROM products WHERE products.name IN ('User external')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_blocks (name, description, tag, status) VALUES ('UserGroupBlock', 'user group block', 'UGB', 'active') RETURNING product_blocks.product_block_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_blocks (name, description, tag, status) VALUES ('UserBlock', 'user block', 'UB', 'active') RETURNING product_blocks.product_block_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('age', 'age of the user') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('username', 'name of the user') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('user_id', 'id of the user') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('group_name', 'name of the user group') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO resource_types (resource_type, description) VALUES ('group_id', 'id of the user group') RETURNING resource_types.resource_type_id
    """))
    conn.execute(sa.text("""
INSERT INTO product_product_blocks (product_id, product_block_id) VALUES ((SELECT products.product_id FROM products WHERE products.name IN ('User Group')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_product_blocks (product_id, product_block_id) VALUES ((SELECT products.product_id FROM products WHERE products.name IN ('User internal')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock'))), ((SELECT products.product_id FROM products WHERE products.name IN ('User external')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_relations (in_use_by_id, depends_on_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')), (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_name')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_id')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('username')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('age')))
    """))
    conn.execute(sa.text("""
INSERT INTO product_block_resource_types (product_block_id, resource_type_id) VALUES ((SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')), (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('user_id')))
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_name'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_name'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('group_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('username'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('username'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('age'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('age'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_resource_types WHERE product_block_resource_types.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('user_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values USING product_block_resource_types WHERE subscription_instance_values.subscription_instance_id IN (SELECT subscription_instances.subscription_instance_id FROM subscription_instances WHERE subscription_instances.subscription_instance_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock'))) AND product_block_resource_types.resource_type_id = (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('user_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instance_values WHERE subscription_instance_values.resource_type_id IN (SELECT resource_types.resource_type_id FROM resource_types WHERE resource_types.resource_type IN ('age', 'username', 'user_id', 'group_name', 'group_id'))
    """))
    conn.execute(sa.text("""
DELETE FROM resource_types WHERE resource_types.resource_type IN ('age', 'username', 'user_id', 'group_name', 'group_id')
    """))
    conn.execute(sa.text("""
DELETE FROM product_product_blocks WHERE product_product_blocks.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User Group')) AND product_product_blocks.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_product_blocks WHERE product_product_blocks.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User external')) AND product_product_blocks.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_block_relations WHERE product_block_relations.in_use_by_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock')) AND product_block_relations.depends_on_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserGroupBlock'))
    """))
    conn.execute(sa.text("""
DELETE FROM fixed_inputs WHERE fixed_inputs.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User external')) AND fixed_inputs.name = 'affiliation'
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.product_block_id IN (SELECT product_blocks.product_block_id FROM product_blocks WHERE product_blocks.name IN ('UserBlock', 'UserGroupBlock'))
    """))
    conn.execute(sa.text("""
DELETE FROM product_blocks WHERE product_blocks.name IN ('UserBlock', 'UserGroupBlock')
    """))
    conn.execute(sa.text("""
DELETE FROM processes WHERE processes.pid IN (SELECT processes_subscriptions.pid FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User Group', 'User external'))))
    """))
    conn.execute(sa.text("""
DELETE FROM processes_subscriptions WHERE processes_subscriptions.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User Group', 'User external')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscription_instances WHERE subscription_instances.subscription_id IN (SELECT subscriptions.subscription_id FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User Group', 'User external')))
    """))
    conn.execute(sa.text("""
DELETE FROM subscriptions WHERE subscriptions.product_id IN (SELECT products.product_id FROM products WHERE products.name IN ('User internal', 'User Group', 'User external'))
    """))
    conn.execute(sa.text("""
DELETE FROM products WHERE products.name IN ('User internal', 'User Group', 'User external')
    """))
