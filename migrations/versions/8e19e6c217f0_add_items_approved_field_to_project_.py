"""Add items_approved field to Project model

Revision ID: 8e19e6c217f0
Revises: d8f02e8ff71b
Create Date: 2024-04-10 13:48:18.188162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e19e6c217f0'
down_revision = 'd8f02e8ff71b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('items_approved', sa.String(), nullable=True))

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('regno',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('regno',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True,
               autoincrement=True)

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('items_approved')

    # ### end Alembic commands ###
