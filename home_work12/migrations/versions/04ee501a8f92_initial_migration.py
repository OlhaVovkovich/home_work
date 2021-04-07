"""Initial migration.

Revision ID: 04ee501a8f92
Revises: 531dc22edfa6
Create Date: 2021-04-07 23:18:51.833995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04ee501a8f92'
down_revision = '531dc22edfa6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('creation_time', sa.String(length=255), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('settlement_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('time', sa.String(length=30), nullable=True),
    sa.Column('pet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pet_id'], ['pet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activities')
    op.drop_table('pet')
    op.drop_table('order_line')
    op.drop_table('order')
    # ### end Alembic commands ###