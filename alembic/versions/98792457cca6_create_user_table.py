"""create user table

Revision ID: 98792457cca6
Revises: 8181a9f09373
Create Date: 2024-10-23 12:38:07.802149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98792457cca6'
down_revision: Union[str, None] = '8181a9f09373'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
        sa.Column('id',sa.Integer(),nullable=False),
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
