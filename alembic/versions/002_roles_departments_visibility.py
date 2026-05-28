"""roles, department FK, comment XOR, visibility grants

Revision ID: 002
Revises: 001
Create Date: 2026-05-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("department_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_users_department_id",
        "users",
        "departments",
        ["department_id"],
        ["id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            """
            UPDATE users u
            SET department_id = d.id
            FROM departments d
            WHERE u.department IS NOT NULL AND u.department = d.name
            """
        )
    else:
        op.execute(
            """
            UPDATE users
            SET department_id = (
                SELECT id FROM departments WHERE departments.name = users.department
            )
            WHERE department IS NOT NULL
            """
        )

    op.drop_column("users", "department")

    op.execute(
        "UPDATE users SET role = 'admin' WHERE role IN ('Administrator', 'administrator')"
    )
    op.execute(
        "UPDATE users SET role = 'user' WHERE role IN ('Employee', 'Citizen', 'employee', 'citizen')"
    )
    op.execute(
        "UPDATE project_members SET role = 'member' WHERE role IN ('contributor', 'Contributor')"
    )

    op.execute(
        """
        DELETE FROM comments
        WHERE (task_id IS NULL AND project_id IS NULL)
           OR (task_id IS NOT NULL AND project_id IS NOT NULL)
        """
    )
    op.create_check_constraint(
        "ck_comments_task_xor_project",
        "comments",
        "(task_id IS NOT NULL AND project_id IS NULL) OR "
        "(task_id IS NULL AND project_id IS NOT NULL)",
    )

    op.create_table(
        "project_visibility_grants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_visibility_grants_project_user",
        ),
    )
    op.create_index(
        op.f("ix_project_visibility_grants_id"),
        "project_visibility_grants",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_project_visibility_grants_id"),
        table_name="project_visibility_grants",
    )
    op.drop_table("project_visibility_grants")

    op.drop_constraint("ck_comments_task_xor_project", "comments", type_="check")

    op.add_column(
        "users",
        sa.Column("department", sa.String(length=100), nullable=True),
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            """
            UPDATE users u
            SET department = d.name
            FROM departments d
            WHERE u.department_id = d.id
            """
        )
    else:
        op.execute(
            """
            UPDATE users
            SET department = (
                SELECT name FROM departments WHERE departments.id = users.department_id
            )
            WHERE department_id IS NOT NULL
            """
        )

    op.execute(
        "UPDATE users SET role = 'Administrator' WHERE role = 'admin'"
    )
    op.execute(
        "UPDATE users SET role = 'Employee' WHERE role = 'user'"
    )

    op.drop_constraint("fk_users_department_id", "users", type_="foreignkey")
    op.drop_column("users", "department_id")
