"""add user table

Revision ID: 174687ae04d6
Revises: 9981b92cf10f
Create Date: 2023-06-21 02:21:12.268856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '174687ae04d6'
down_revision = '9981b92cf10f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
