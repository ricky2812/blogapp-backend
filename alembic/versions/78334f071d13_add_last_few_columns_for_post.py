"""add last few columns for post

Revision ID: 78334f071d13
Revises: c56752adf289
Create Date: 2023-06-21 02:32:41.503961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78334f071d13'
down_revision = 'c56752adf289'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
