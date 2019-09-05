"""empty message

Revision ID: f276c9e8a42a
Revises: 69764b02ad9c
Create Date: 2019-09-04 17:13:10.312818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f276c9e8a42a'
down_revision = '69764b02ad9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staffs', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staffs', sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
