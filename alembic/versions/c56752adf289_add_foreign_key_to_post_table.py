"""add foreign key to post table

Revision ID: c56752adf289
Revises: 174687ae04d6
Create Date: 2023-06-21 02:28:14.142975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c56752adf289'
down_revision = '174687ae04d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_owner_id', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('fk_posts_owner_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
