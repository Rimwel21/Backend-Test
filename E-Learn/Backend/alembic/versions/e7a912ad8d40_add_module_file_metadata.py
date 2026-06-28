"""add module file metadata

Revision ID: e7a912ad8d40
Revises: d1e6b27f3b91
Create Date: 2026-06-27 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e7a912ad8d40"
down_revision: Union[str, Sequence[str], None] = "d1e6b27f3b91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("teacher_modules", sa.Column("file_name", sa.String(length=255), nullable=True))
    op.add_column("teacher_modules", sa.Column("file_type", sa.String(length=120), nullable=True))


def downgrade() -> None:
    op.drop_column("teacher_modules", "file_type")
    op.drop_column("teacher_modules", "file_name")
