"""add foreign-key to post table

Revision ID: 1fd93b7eb85f
Revises: eeb4e6b58e51
Create Date: 2026-07-04 23:44:13.500558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fd93b7eb85f'
down_revision: Union[str, Sequence[str], None] = 'eeb4e6b58e51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_owner_id_fkey',
        'posts', 'users',
        ['owner_id'], ['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
