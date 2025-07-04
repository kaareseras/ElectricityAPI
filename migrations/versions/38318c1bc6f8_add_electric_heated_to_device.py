"""add electric heated to device

Revision ID: 38318c1bc6f8
Revises: 5092328011ed
Create Date: 2025-06-24 20:51:32.491189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38318c1bc6f8'
down_revision: Union[str, None] = '5092328011ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('is_electric_heated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'is_electric_heated')
    # ### end Alembic commands ###
