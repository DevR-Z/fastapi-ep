"""add last few columns to post table

Revision ID: 495f471385a0
Revises: a4acdbde0c5a
Create Date: 2024-10-23 13:11:27.033621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '495f471385a0'
down_revision: Union[str, None] = 'a4acdbde0c5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',
        sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('post',
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('post','published')
    op.drop_column('post','created_at')
    pass
