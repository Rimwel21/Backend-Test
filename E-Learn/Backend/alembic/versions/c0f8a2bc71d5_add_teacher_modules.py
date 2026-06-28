"""add teacher modules

Revision ID: c0f8a2bc71d5
Revises: 8f3b2d11a724
Create Date: 2026-06-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c0f8a2bc71d5"
down_revision: Union[str, Sequence[str], None] = "8f3b2d11a724"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teacher_modules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["teacher_classes.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["teacher_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teacher_modules_class_id"), "teacher_modules", ["class_id"], unique=False)
    op.create_index(op.f("ix_teacher_modules_id"), "teacher_modules", ["id"], unique=False)
    op.create_index(op.f("ix_teacher_modules_teacher_id"), "teacher_modules", ["teacher_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_teacher_modules_teacher_id"), table_name="teacher_modules")
    op.drop_index(op.f("ix_teacher_modules_id"), table_name="teacher_modules")
    op.drop_index(op.f("ix_teacher_modules_class_id"), table_name="teacher_modules")
    op.drop_table("teacher_modules")
