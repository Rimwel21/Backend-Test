"""add material fields and assessments

Revision ID: d1e6b27f3b91
Revises: c0f8a2bc71d5
Create Date: 2026-06-27 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d1e6b27f3b91"
down_revision: Union[str, Sequence[str], None] = "c0f8a2bc71d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("teacher_modules", sa.Column("content_type", sa.String(length=60), nullable=True))
    op.add_column("teacher_modules", sa.Column("week", sa.String(length=30), nullable=True))
    op.add_column("teacher_modules", sa.Column("behavior_required", sa.String(length=10), nullable=False, server_default="true"))
    op.add_column("teacher_modules", sa.Column("estimated_time", sa.String(length=30), nullable=True))
    op.create_table(
        "teacher_assessments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("assessment_type", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=True),
        sa.Column("week", sa.String(length=30), nullable=True),
        sa.Column("time_limit", sa.String(length=30), nullable=True),
        sa.Column("attempts_allowed", sa.Integer(), nullable=False),
        sa.Column("shuffle_questions", sa.String(length=10), nullable=False),
        sa.Column("show_answers_after_submission", sa.String(length=10), nullable=False),
        sa.Column("questions", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teacher_assessments_assessment_type"), "teacher_assessments", ["assessment_type"], unique=False)
    op.create_index(op.f("ix_teacher_assessments_id"), "teacher_assessments", ["id"], unique=False)
    op.create_index(op.f("ix_teacher_assessments_teacher_id"), "teacher_assessments", ["teacher_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_teacher_assessments_teacher_id"), table_name="teacher_assessments")
    op.drop_index(op.f("ix_teacher_assessments_id"), table_name="teacher_assessments")
    op.drop_index(op.f("ix_teacher_assessments_assessment_type"), table_name="teacher_assessments")
    op.drop_table("teacher_assessments")
    op.drop_column("teacher_modules", "estimated_time")
    op.drop_column("teacher_modules", "behavior_required")
    op.drop_column("teacher_modules", "week")
    op.drop_column("teacher_modules", "content_type")
