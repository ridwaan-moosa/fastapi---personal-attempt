"""add_columns_to_posts2

Revision ID: 7c970b397215
Revises: a8fd4f5f88bb
Create Date: 2022-08-18 14:58:21.046464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c970b397215'
down_revision = 'a8fd4f5f88bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts2', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts2', 'published')
    op.drop_column('posts2', 'created_at')
    pass
