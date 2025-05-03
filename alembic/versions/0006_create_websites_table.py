from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "websites",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String, nullable=False, unique=True, index=True),
        sa.Column("title", sa.String, nullable=True),
        sa.Column("icon", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("websites")
