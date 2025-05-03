from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "torrent_websites",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String, nullable=False, unique=True, index=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("icon", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("torrent_websites")
