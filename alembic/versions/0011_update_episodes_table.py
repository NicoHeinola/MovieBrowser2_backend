from alembic import op
import sqlalchemy as sa

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("episodes", sa.Column("file_size_bytes", sa.BigInteger, nullable=True))


def downgrade():
    op.drop_column("episodes", "file_size_bytes")
