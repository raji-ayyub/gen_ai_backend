"""alter table users

Revision ID: af69b29806ad
Revises: 
Create Date: 2025-10-23 12:04:41.124655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af69b29806ad'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE users
    ADD COLMN userType varchar(100) DEFAULT 'student'
    """)
    pass


def downgrade() -> None:
    op.execute("""
    ALTER TABLE users
    DROP COLUMN userType

    """)
    pass
