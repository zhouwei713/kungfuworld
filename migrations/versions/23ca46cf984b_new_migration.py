"""new migration

Revision ID: 23ca46cf984b
Revises: 161387674862
Create Date: 2019-03-25 19:36:15.227200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23ca46cf984b'
down_revision = '161387674862'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('novelname', sa.String(length=128), nullable=True))
    op.drop_column('posts', 'novel_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('novel_name', sa.VARCHAR(length=128), nullable=True))
    op.drop_column('posts', 'novelname')
    # ### end Alembic commands ###