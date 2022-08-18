"""create_new_column

Revision ID: c8f836f867c0
Revises: e3bbd424945f
Create Date: 2022-08-18 14:37:04.660980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f836f867c0'
down_revision = 'e3bbd424945f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('context', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    pass
