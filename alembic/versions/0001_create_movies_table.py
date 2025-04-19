from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("director", sa.String, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("movies")
