"""add teacher classes

Revision ID: 8f3b2d11a724
Revises: 2118047d37c9
Create Date: 2026-06-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f3b2d11a724"
down_revision: Union[str, Sequence[str], None] = "2118047d37c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "teacher_classes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("grade_level", sa.String(length=30), nullable=False),
        sa.Column("section", sa.String(length=50), nullable=False),
        sa.Column("student_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("teacher_id", "grade_level", "section", name="uq_teacher_class_grade_section"),
    )
    op.create_index(op.f("ix_teacher_classes_id"), "teacher_classes", ["id"], unique=False)
    op.create_index(op.f("ix_teacher_classes_teacher_id"), "teacher_classes", ["teacher_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_teacher_classes_teacher_id"), table_name="teacher_classes")
    op.drop_index(op.f("ix_teacher_classes_id"), table_name="teacher_classes")
    op.drop_table("teacher_classes")
