"""create delete_cancel_order_tables trigger

Revision ID: 276fa89710e3
Revises: 425470359914
Create Date: 2021-04-18 17:12:05.585282

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "276fa89710e3"
down_revision = "425470359914"
branch_labels = None
depends_on = None


TRIGGER_FUNCTION = "delete_order_tables"
TRIGGER_NAME = "delete_cancel_order_tables"


def upgrade():
    # create trigger function
    op.execute(
        f"""
        CREATE FUNCTION {TRIGGER_FUNCTION}() RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM table_availability WHERE order_id IN (SELECT id FROM public.order WHERE ref_id = NEW.ref_id);
                RETURN NEW;
            END;
        $$ LANGUAGE plpgsql;
    """
    )
    # create trigger
    op.execute(
        f"""
        CREATE TRIGGER {TRIGGER_NAME}
            AFTER UPDATE ON public.order
        FOR EACH ROW
            WHEN (NEW.status = 'cancelled')
            EXECUTE PROCEDURE delete_order_tables();
    """
    )


def downgrade():
    # drop trigger on table public.order
    op.execute(
        f"""
        drop trigger delete_cancel_order_tables on "order";
    """
    )
    # drop trigger function
    op.execute(
        f"""
        drop function delete_order_tables();
    """
    )
