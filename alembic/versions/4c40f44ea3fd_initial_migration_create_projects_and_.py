"""initial migration: create projects and tasks tables

Revision ID: 4c40f44ea3fd
Revises: 
Create Date: 2025-11-22 23:20:15.892210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c40f44ea3fd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create projects table
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=150), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_project_name"),
    )

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=150), nullable=False),
        sa.Column(
            "status",
            sa.String(length=10),
            server_default="todo",
            nullable=False,
        ),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "status IN ('todo', 'doing', 'done')",
            name="check_task_status",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
    op.drop_table("projects")
