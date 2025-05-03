from alembic import op
import sqlalchemy as sa

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "website_tags",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column(
            "website_id", sa.Integer, sa.ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.UniqueConstraint("website_id", "name", name="uq_website_tag"),
    )


def downgrade():
    op.drop_table("website_tags")
