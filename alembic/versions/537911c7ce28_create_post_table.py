"""create post table

Revision ID: 537911c7ce28
Revises: 
Create Date: 2024-10-23 12:10:06.779246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '537911c7ce28'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('post',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
        sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op,drop_table('post')
    pass
