"""datetime to date

Revision ID: 835911d23acc
Revises: d8beabcb2a3f
Create Date: 2024-05-18 20:33:14.338052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '835911d23acc'
down_revision: Union[str, None] = 'd8beabcb2a3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'event_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'event_date',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###
