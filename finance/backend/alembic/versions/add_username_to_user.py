"""add username to user

Revision ID: e1faad9c7559
Revises: 
Create Date: 2023-10-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1faad9c7559'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add username column to user table with a default value to handle existing users
    op.add_column('user', sa.Column('username', sa.String(), nullable=True))
    
    # Create a temporary unique index on username
    op.execute("UPDATE user SET username = CONCAT('user_', id) WHERE username IS NULL")
    
    # Set the column to not nullable after populating values
    op.alter_column('user', 'username', nullable=False)
    
    # Create an index on username
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)


def downgrade():
    # Remove the index first
    op.drop_index(op.f('ix_user_username'), table_name='user')
    
    # Remove the column
    op.drop_column('user', 'username') 