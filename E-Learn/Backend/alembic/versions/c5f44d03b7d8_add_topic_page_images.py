"""add topic page images

Revision ID: c5f44d03b7d8
Revises: b2c61e7f4a90
Create Date: 2026-06-28 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c5f44d03b7d8"
down_revision: Union[str, None] = "b2c61e7f4a90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("learning_topics", sa.Column("page_image_urls", sa.JSON(), nullable=False, server_default="[]"))
    op.alter_column("learning_topics", "page_image_urls", server_default=None)


def downgrade() -> None:
    op.drop_column("learning_topics", "page_image_urls")
