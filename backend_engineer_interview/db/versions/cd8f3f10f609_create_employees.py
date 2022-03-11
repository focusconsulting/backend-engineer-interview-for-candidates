"""Create employees

Revision ID: cd8f3f10f609
Revises: 11b7d12c8562
Create Date: 2022-03-10 23:18:06.056872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cd8f3f10f609"
down_revision = "11b7d12c8562"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO employee VALUES (1, 'John', 'Lennon', '1940-10-04', 'a')")
    op.execute("INSERT INTO employee VALUES (2, 'Rino', 'Star', '1940-07-07', 'b')")
    op.execute("INSERT INTO  employee VALUES (10, 'Rino', 'Star', '1940-07-07', 'c')")


def downgrade():
    pass
