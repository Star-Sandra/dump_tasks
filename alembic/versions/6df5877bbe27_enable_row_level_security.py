"""enable row level security

Revision ID: 6df5877bbe27
Revises: 8e2a4def583c
Create Date: 2026-10-19 11:24:21.113273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '6df5877bbe27'
down_revision: Union[str, Sequence[str], None] = '8e2a4def583c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in ("users", "task_sources", "tasks"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    for table in ("users", "task_sources", "tasks"):
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
