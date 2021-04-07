"""Initial migration.

Revision ID: a719b7e08e23
Revises: 
Create Date: 2021-03-16 21:52:52.531849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a719b7e08e23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=6), nullable=False),
    sa.Column('telephone', sa.String(length=13), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telephone'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
