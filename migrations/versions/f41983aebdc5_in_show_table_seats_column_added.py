"""in show table seats column added

Revision ID: f41983aebdc5
Revises: 808421fba6fd
Create Date: 2023-03-27 16:24:20.191817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f41983aebdc5'
down_revision = '808421fba6fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available_seats', sa.Integer(), nullable=False))
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('available_seats')

    # ### end Alembic commands ###