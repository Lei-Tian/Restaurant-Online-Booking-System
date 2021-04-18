"""add restaurant table capacity constraint

Revision ID: fd348661994b
Revises: 276fa89710e3
Create Date: 2021-04-18 17:46:51.796901

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fd348661994b"
down_revision = "276fa89710e3"
branch_labels = None
depends_on = None


TABLE_NAME = "restaurant_table"
CONSTRAINT_NAME = "check_table_capacity_range"


def upgrade():
    op.execute(
        f"""
        ALTER TABLE {TABLE_NAME}
        ADD CONSTRAINT {CONSTRAINT_NAME} CHECK (capacity > 0 AND capacity <= 8);
    """
    )


def downgrade():
    op.execute(
        f"""
        ALTER TABLE {TABLE_NAME}
            DROP CONSTRAINT {CONSTRAINT_NAME};
    """
    )
