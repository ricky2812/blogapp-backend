"""create posts table

Revision ID: 55b1f84dc5f0
Revises: 
Create Date: 2023-06-21 02:09:14.193167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55b1f84dc5f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable=False)
    )
    


def downgrade() -> None:
    op.drop_table('posts')
