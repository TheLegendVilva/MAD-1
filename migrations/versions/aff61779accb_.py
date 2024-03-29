"""empty message

Revision ID: aff61779accb
Revises: 14801fac2594
Create Date: 2023-04-23 19:13:02.188895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aff61779accb'
down_revision = '14801fac2594'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.FLOAT(),
               nullable=False,
               existing_server_default=sa.text('0'))
        batch_op.alter_column('tags',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('show_timing',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('user_hist_rating', schema=None) as batch_op:
        batch_op.alter_column('user_rating',
               existing_type=sa.FLOAT(),
               nullable=False,
               existing_server_default=sa.text('0'))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=True)

    with op.batch_alter_table('user_hist_rating', schema=None) as batch_op:
        batch_op.alter_column('user_rating',
               existing_type=sa.FLOAT(),
               nullable=True,
               existing_server_default=sa.text('0'))

    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('show_timing',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('tags',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('rating',
               existing_type=sa.FLOAT(),
               nullable=True,
               existing_server_default=sa.text('0'))

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###
