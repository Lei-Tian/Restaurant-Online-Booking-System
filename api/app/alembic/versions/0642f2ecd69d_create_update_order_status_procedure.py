"""create search location store procedure

Revision ID: 0642f2ecd69d
Revises: fd348661994b
Create Date: 2021-04-24 13:02:15.702992

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0642f2ecd69d"
down_revision = "fd348661994b"
branch_labels = None
depends_on = None


PROCEDURE_NAME = "update_order_status"


def upgrade():
    # create procedure
    op.execute(
        f"""
        CREATE PROCEDURE {PROCEDURE_NAME}(status_param orderstatus, ref_id_param varchar) LANGUAGE PLPGSQL AS $$
            BEGIN
                UPDATE public.order SET status = status_param where ref_id = ref_id_param;
            END
        $$;
    """
    )


def downgrade():
    # drop procedure
    op.execute(f"DROP PROCEDURE {PROCEDURE_NAME}(orderstatus, varchar);")
