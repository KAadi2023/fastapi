"""add content column

Revision ID: 3423a19bec7d
Revises: fe6b9cd95b3d
Create Date: 2026-07-04 23:23:12.554184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3423a19bec7d'
down_revision: Union[str, Sequence[str], None] = 'fe6b9cd95b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
