"""link assessments to modules

Revision ID: b2c61e7f4a90
Revises: f17c4d92a8b2
Create Date: 2026-06-27 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b2c61e7f4a90"
down_revision: Union[str, None] = "f17c4d92a8b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("teacher_assessments", sa.Column("module_id", sa.Integer(), nullable=True))
    op.add_column("teacher_assessments", sa.Column("topic_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_teacher_assessments_module_id"), "teacher_assessments", ["module_id"], unique=False)
    op.create_index(op.f("ix_teacher_assessments_topic_id"), "teacher_assessments", ["topic_id"], unique=False)
    op.create_foreign_key("fk_teacher_assessments_module_id", "teacher_assessments", "teacher_modules", ["module_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_teacher_assessments_topic_id", "teacher_assessments", "learning_topics", ["topic_id"], ["id"], ondelete="SET NULL")

    op.create_table(
        "student_quiz_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assessment_id"], ["teacher_assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["module_id"], ["teacher_modules.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "assessment_id", name="uq_student_quiz_progress"),
    )
    op.create_index(op.f("ix_student_quiz_progress_assessment_id"), "student_quiz_progress", ["assessment_id"], unique=False)
    op.create_index(op.f("ix_student_quiz_progress_id"), "student_quiz_progress", ["id"], unique=False)
    op.create_index(op.f("ix_student_quiz_progress_module_id"), "student_quiz_progress", ["module_id"], unique=False)
    op.create_index(op.f("ix_student_quiz_progress_student_id"), "student_quiz_progress", ["student_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_student_quiz_progress_student_id"), table_name="student_quiz_progress")
    op.drop_index(op.f("ix_student_quiz_progress_module_id"), table_name="student_quiz_progress")
    op.drop_index(op.f("ix_student_quiz_progress_id"), table_name="student_quiz_progress")
    op.drop_index(op.f("ix_student_quiz_progress_assessment_id"), table_name="student_quiz_progress")
    op.drop_table("student_quiz_progress")
    op.drop_constraint("fk_teacher_assessments_topic_id", "teacher_assessments", type_="foreignkey")
    op.drop_constraint("fk_teacher_assessments_module_id", "teacher_assessments", type_="foreignkey")
    op.drop_index(op.f("ix_teacher_assessments_topic_id"), table_name="teacher_assessments")
    op.drop_index(op.f("ix_teacher_assessments_module_id"), table_name="teacher_assessments")
    op.drop_column("teacher_assessments", "topic_id")
    op.drop_column("teacher_assessments", "module_id")
