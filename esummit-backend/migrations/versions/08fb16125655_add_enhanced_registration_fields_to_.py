"""Add enhanced registration fields to ensure they exist in the database

Revision ID: 08fb16125655
Revises: 1e171ece3db3
Create Date: 2025-03-30 15:39:01.794675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08fb16125655'
down_revision = '1e171ece3db3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prize_pool', sa.Integer(), nullable=True))

    with op.batch_alter_table('event_registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('institution', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('why_join', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('experience', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('document_filename', sa.String(length=255), nullable=True))

    with op.batch_alter_table('hackathon_registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('proposal_document_filename', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('problem_statement', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('solution_approach', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('team_background', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hackathon_registration', schema=None) as batch_op:
        batch_op.drop_column('team_background')
        batch_op.drop_column('solution_approach')
        batch_op.drop_column('problem_statement')
        batch_op.drop_column('proposal_document_filename')

    with op.batch_alter_table('event_registration', schema=None) as batch_op:
        batch_op.drop_column('document_filename')
        batch_op.drop_column('experience')
        batch_op.drop_column('why_join')
        batch_op.drop_column('institution')
        batch_op.drop_column('phone')
        batch_op.drop_column('email')
        batch_op.drop_column('full_name')

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('prize_pool')

    # ### end Alembic commands ###
