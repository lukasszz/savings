"""Budget icon

Revision ID: 778c05fb106e
Revises: 
Create Date: 2020-05-25 17:17:58.172935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '778c05fb106e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('budget', sa.Column('icon', sa.Text))


def downgrade():
    pass
