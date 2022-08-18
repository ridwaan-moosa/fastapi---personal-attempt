"""create_users_table

Revision ID: 07ec6dac924e
Revises: c8f836f867c0
Create Date: 2022-08-18 14:40:18.609127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ec6dac924e'
down_revision = 'c8f836f867c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users2',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users2')
    pass
