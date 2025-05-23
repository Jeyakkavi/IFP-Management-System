"""Initial migration

Revision ID: e570c830c3e4
Revises: 
Create Date: 2024-03-16 01:16:59.426182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e570c830c3e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('domain', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('sanction_copy', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('academic_year', sa.String(length=20), nullable=True))
        #batch_op.add_column(sa.Column('student_year', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        #batch_op.drop_column('student_year')
        batch_op.drop_column('academic_year')
        batch_op.drop_column('sanction_copy')
        batch_op.drop_column('domain')

    # ### end Alembic commands ###
