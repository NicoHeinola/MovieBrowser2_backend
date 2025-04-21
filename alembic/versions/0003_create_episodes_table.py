from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "episodes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("season_id", sa.Integer, sa.ForeignKey("seasons.id"), nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("type", sa.String, nullable=True),  # New column added
    )


def downgrade():
    op.drop_table("episodes")
