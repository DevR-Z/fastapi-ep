"""add foreign key to post table

Revision ID: a4acdbde0c5a
Revises: 98792457cca6
Create Date: 2024-10-23 13:03:01.434152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4acdbde0c5a'
down_revision: Union[str, None] = '98792457cca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',
        sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table='post',referent_table='user',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='post')
    op.drop_column('post','owner_id')
    pass
