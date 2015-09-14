"""create account table

Revision ID: 28b3ecc456f6
Revises: 
Create Date: 2015-09-14 04:12:38.560305

"""

# revision identifiers, used by Alembic.
revision = '28b3ecc456f6'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column


def upgrade():
    op.create_table('tmp', Column('id', INTEGER, primary_key=True))


def downgrade():
    op.drop_table('tmp')
