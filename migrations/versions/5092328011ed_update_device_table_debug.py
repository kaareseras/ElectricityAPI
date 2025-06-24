"""update device table debug

Revision ID: 5092328011ed
Revises: 6f9677509fc5
Create Date: 2025-06-23 12:50:12.226419

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5092328011ed"
down_revision: Union[str, None] = "6f9677509fc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Explicit cast using USING clause
    op.execute("""
        ALTER TABLE device
        ALTER COLUMN is_adopted TYPE BOOLEAN
        USING is_adopted::BOOLEAN;
    """)
    op.execute("""
        ALTER TABLE device
        ALTER COLUMN is_blocked TYPE BOOLEAN
        USING is_blocked::BOOLEAN;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to INTEGER explicitly
    op.execute("""
        ALTER TABLE device
        ALTER COLUMN is_blocked TYPE INTEGER
        USING is_blocked::INTEGER;
    """)
    op.execute("""
        ALTER TABLE device
        ALTER COLUMN is_adopted TYPE INTEGER
        USING is_adopted::INTEGER;
    """)
    # ### end Alembic commands ###
