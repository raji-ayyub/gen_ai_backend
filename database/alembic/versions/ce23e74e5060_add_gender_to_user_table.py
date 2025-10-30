"""add gender to user table

Revision ID: ce23e74e5060
Revises: f150a7e4fc21
Create Date: 2025-10-27 11:54:29.914417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce23e74e5060'
down_revision: Union[str, Sequence[str], None] = 'f150a7e4fc21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users
        ADD COLUMN gender VARCHAR(10)
    """)


def downgrade() -> None:
    """
    ALTER TABLE users
    DROP COLUMN gender
    
    """