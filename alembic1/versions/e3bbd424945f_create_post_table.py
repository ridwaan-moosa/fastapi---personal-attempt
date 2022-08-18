"""create post table

Revision ID: e3bbd424945f
Revises: 
Create Date: 2022-08-18 14:03:34.924054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3bbd424945f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts2', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),sa.Column('tittle', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts2')
    pass
