"""add user and usergroup workflows.

Revision ID: 130cb51287a4
Revises: 94d04a8973c0
Create Date: 2023-10-03 16:41:06.901425

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '130cb51287a4'
down_revision = '9a31b6bf3e85'
branch_labels = None
depends_on = None


from orchestrator.migrations.helpers import create_workflow, delete_workflow

new_workflows = [
    {
        "name": "create_user_group",
        "target": "CREATE",
        "description": "Create user group",
        "product_type": "UserGroup"
    },
    {
        "name": "modify_user_group",
        "target": "MODIFY",
        "description": "Modify user group",
        "product_type": "UserGroup"
    },
    {
        "name": "terminate_user_group",
        "target": "TERMINATE",
        "description": "Terminate user group",
        "product_type": "UserGroup"
    },
    {
        "name": "create_user",
        "target": "CREATE",
        "description": "Create user",
        "product_type": "User"
    },
    {
        "name": "modify_user",
        "target": "MODIFY",
        "description": "Modify user",
        "product_type": "User"
    },
    {
        "name": "terminate_user",
        "target": "TERMINATE",
        "description": "Terminate user",
        "product_type": "User"
    }
]


def upgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        create_workflow(conn, workflow)


def downgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        delete_workflow(conn, workflow["name"])
