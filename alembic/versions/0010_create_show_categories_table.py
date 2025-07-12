from alembic import op
import sqlalchemy as sa

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "show_categories",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("show_id", sa.Integer, sa.ForeignKey("shows.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String, nullable=False),
        sa.UniqueConstraint("show_id", "name", name="uq_show_category"),
    )


def downgrade():
    op.drop_table("show_categories")
