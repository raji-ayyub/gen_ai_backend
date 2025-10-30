"""initial setup

Revision ID: f150a7e4fc21
Revises: 
Create Date: 2025-10-27 11:49:15.117259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f150a7e4fc21'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            usertype VARCHAR(50) NOT NULL
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS users;")
