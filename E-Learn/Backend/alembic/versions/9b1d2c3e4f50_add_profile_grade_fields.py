"""add profile grade fields

Revision ID: 9b1d2c3e4f50
Revises: c5f44d03b7d8
Create Date: 2026-07-03 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


revision: str = "9b1d2c3e4f50"
down_revision: Union[str, Sequence[str], None] = "c5f44d03b7d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    usersex_enum = postgresql.ENUM("Male", "Female", name="usersex")
    gradelevel_enum = postgresql.ENUM(
        "grade_1",
        "grade_2",
        "grade_3",
        "grade_4",
        "grade_5",
        "grade_6",
        name="gradelevel",
    )

    usersex_enum.create(op.get_bind(), checkfirst=True)
    gradelevel_enum.create(op.get_bind(), checkfirst=True)
    usersex_type = postgresql.ENUM("Male", "Female", name="usersex", create_type=False)
    gradelevel_type = postgresql.ENUM(
        "grade_1",
        "grade_2",
        "grade_3",
        "grade_4",
        "grade_5",
        "grade_6",
        name="gradelevel",
        create_type=False,
    )

    op.add_column("student_profiles", sa.Column("age", sa.Integer(), nullable=True))
    op.add_column("student_profiles", sa.Column("sex", usersex_type, nullable=True))
    op.add_column(
        "student_profiles",
        sa.Column("grade_level", gradelevel_type, nullable=True),
    )
    op.add_column("student_profiles", sa.Column("section", sa.String(length=250), nullable=True))
    op.add_column("teacher_profiles", sa.Column("age", sa.Integer(), nullable=True))
    op.add_column("teacher_profiles", sa.Column("sex", usersex_type, nullable=True))

    op.create_table(
        "teacher_grade_handles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("grade_level_handles", gradelevel_type, nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["teacher_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teacher_grade_handles_id"), "teacher_grade_handles", ["id"], unique=True)
    op.create_index(op.f("ix_teacher_grade_handles_teacher_id"), "teacher_grade_handles", ["teacher_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_teacher_grade_handles_teacher_id"), table_name="teacher_grade_handles")
    op.drop_index(op.f("ix_teacher_grade_handles_id"), table_name="teacher_grade_handles")
    op.drop_table("teacher_grade_handles")
    op.drop_column("teacher_profiles", "sex")
    op.drop_column("teacher_profiles", "age")
    op.drop_column("student_profiles", "section")
    op.drop_column("student_profiles", "grade_level")
    op.drop_column("student_profiles", "sex")
    op.drop_column("student_profiles", "age")

    postgresql.ENUM(name="gradelevel").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="usersex").drop(op.get_bind(), checkfirst=True)
