"""add content posts table

Revision ID: 9981b92cf10f
Revises: 55b1f84dc5f0
Create Date: 2023-06-21 02:17:01.869461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9981b92cf10f'
down_revision = '55b1f84dc5f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
