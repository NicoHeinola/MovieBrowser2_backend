from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "user_watch_seasons",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("season_id", sa.Integer, sa.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("show_id", sa.Integer, sa.ForeignKey("shows.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )


def downgrade():
    op.drop_table("user_watch_seasons")
