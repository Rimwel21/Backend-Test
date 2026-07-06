"""backend test lms compatibility

Revision ID: a7c9e2d4f601
Revises: 9b1d2c3e4f50
Create Date: 2026-07-04 00:00:00.000000

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "a7c9e2d4f601"
down_revision: Union[str, Sequence[str], None] = "9b1d2c3e4f50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Backend-test already has these LMS tables in earlier revisions."""
    pass


def downgrade() -> None:
    """Keep compatibility revision non-destructive."""
    pass
