"""Initial migration

Revision ID: c446abf67870
Revises:
Create Date: 2026-06-08 16:36:15.997706+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "c446abf67870"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column(
            "id", sa.Uuid(), nullable=False, comment="Идентификатор пользователя"
        ),
        sa.Column(
            "is_admin",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
            comment="Права администратора",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="account",
    )
    op.create_table(
        "last_login",
        sa.Column(
            "user_id", sa.Uuid(), nullable=False, comment="Идентификатор пользователя"
        ),
        sa.Column(
            "last_login", sa.DateTime(), nullable=True, comment="Время последнего входа"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["account.user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
        schema="account",
    )


def downgrade():
    op.drop_table("last_login", schema="account")
    op.drop_table("user", schema="account")
