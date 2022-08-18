"""add_f_key_to_posts2_table

Revision ID: a8fd4f5f88bb
Revises: 07ec6dac924e
Create Date: 2022-08-18 14:49:56.098918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8fd4f5f88bb'
down_revision = '07ec6dac924e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts2", referent_table="users2", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts2")
    op.drop_column('posts2', 'owner_id')
    pass
