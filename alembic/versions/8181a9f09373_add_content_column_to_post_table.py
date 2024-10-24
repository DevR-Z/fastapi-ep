"""add content column to post table

Revision ID: 8181a9f09373
Revises: 537911c7ce28
Create Date: 2024-10-23 12:28:08.372727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8181a9f09373'
down_revision: Union[str, None] = '537911c7ce28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post','content')
    pass
