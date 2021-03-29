"""add booking_time to Order table

Revision ID: 08431ff2fa21
Revises: 7a0316c80783
Create Date: 2021-03-28 21:17:55.599249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08431ff2fa21'
down_revision = '7a0316c80783'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('booking_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'booking_time')
    # ### end Alembic commands ###