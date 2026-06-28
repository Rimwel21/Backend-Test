"""add learning topics and progress

Revision ID: f17c4d92a8b2
Revises: e7a912ad8d40
Create Date: 2026-06-27 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f17c4d92a8b2"
down_revision: Union[str, None] = "e7a912ad8d40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("teacher_modules", sa.Column("file_path", sa.String(length=500), nullable=True))
    op.add_column("teacher_modules", sa.Column("file_size", sa.Integer(), nullable=True))

    op.create_table(
        "learning_topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["module_id"], ["teacher_modules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_learning_topics_id"), "learning_topics", ["id"], unique=False)
    op.create_index(op.f("ix_learning_topics_module_id"), "learning_topics", ["module_id"], unique=False)

    op.create_table(
        "student_topic_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["module_id"], ["teacher_modules.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["topic_id"], ["learning_topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "topic_id", name="uq_student_topic_progress"),
    )
    op.create_index(op.f("ix_student_topic_progress_id"), "student_topic_progress", ["id"], unique=False)
    op.create_index(op.f("ix_student_topic_progress_module_id"), "student_topic_progress", ["module_id"], unique=False)
    op.create_index(op.f("ix_student_topic_progress_student_id"), "student_topic_progress", ["student_id"], unique=False)
    op.create_index(op.f("ix_student_topic_progress_topic_id"), "student_topic_progress", ["topic_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_student_topic_progress_topic_id"), table_name="student_topic_progress")
    op.drop_index(op.f("ix_student_topic_progress_student_id"), table_name="student_topic_progress")
    op.drop_index(op.f("ix_student_topic_progress_module_id"), table_name="student_topic_progress")
    op.drop_index(op.f("ix_student_topic_progress_id"), table_name="student_topic_progress")
    op.drop_table("student_topic_progress")
    op.drop_index(op.f("ix_learning_topics_module_id"), table_name="learning_topics")
    op.drop_index(op.f("ix_learning_topics_id"), table_name="learning_topics")
    op.drop_table("learning_topics")
    op.drop_column("teacher_modules", "file_size")
    op.drop_column("teacher_modules", "file_path")
