from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("show_id", sa.Integer, sa.ForeignKey("shows.id"), nullable=False),
        sa.Column("title", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("image", sa.String, nullable=True),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("folder_name", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("seasons")
