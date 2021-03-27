"""add index on restaurant name

Revision ID: 01436a9497e4
Revises: c4f8bae45085
Create Date: 2021-03-26 20:10:57.086274-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01436a9497e4'
down_revision = 'c4f8bae45085'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_restaurant_name'), 'restaurant', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_restaurant_name'), table_name='restaurant')
    # ### end Alembic commands ###
