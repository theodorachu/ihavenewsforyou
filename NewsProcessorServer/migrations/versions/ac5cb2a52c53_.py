"""empty message

Revision ID: ac5cb2a52c53
Revises: bf3afea0edc7
Create Date: 2017-03-05 14:34:05.996863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac5cb2a52c53'
down_revision = 'bf3afea0edc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visits', sa.Column('lastActiveTime', sa.DateTime(), nullable=True))
    op.add_column('visits', sa.Column('state', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('visits', 'state')
    op.drop_column('visits', 'lastActiveTime')
    # ### end Alembic commands ###
