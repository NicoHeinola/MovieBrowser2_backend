from alembic import op
import sqlalchemy as sa

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "user_show_statuses",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("show_id", sa.Integer, sa.ForeignKey("shows.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("user_show_statuses")
