"""remove timezone from TableAvailability.booking_time

Revision ID: 425470359914
Revises: e5ce69cd2697
Create Date: 2021-04-08 23:40:20.033031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '425470359914'
down_revision = 'e5ce69cd2697'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(f'''
        ALTER TABLE table_availability ALTER COLUMN booking_time TYPE timestamp
    ''')


def downgrade():
    op.execute(f'''
        ALTER TABLE table_availability ALTER COLUMN booking_time TYPE timestamp with time zone
    ''')

