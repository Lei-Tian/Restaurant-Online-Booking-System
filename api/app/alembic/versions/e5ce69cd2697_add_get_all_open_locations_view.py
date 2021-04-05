"""add get_all_open_locations view

Revision ID: e5ce69cd2697
Revises: 08431ff2fa21
Create Date: 2021-04-05 14:35:56.807540

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e5ce69cd2697'
down_revision = '08431ff2fa21'
branch_labels = None
depends_on = None

ALL_OPEN_LOCATIONS_VIEW_NAME = 'all_open_locations'

def upgrade():
    op.execute(f'''
        CREATE VIEW {ALL_OPEN_LOCATIONS_VIEW_NAME} AS
            SELECT DISTINCT location_id, city, state, country
            FROM restaurant, location
            where location_id = location.id AND is_open = true
    ''')


def downgrade():
    op.execute(f'''
        DROP VIEW {ALL_OPEN_LOCATIONS_VIEW_NAME}
    ''')
