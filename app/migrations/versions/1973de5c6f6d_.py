"""empty message

Revision ID: 1973de5c6f6d
Revises: 
Create Date: 2017-03-14 19:17:28.739067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1973de5c6f6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('source', sa.String(length=128), nullable=True),
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.Column('bias', sa.String(length=64), nullable=True),
    sa.Column('publishedDate', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.Column('authors', sa.String(length=256), nullable=True),
    sa.Column('keywords', sa.String(length=256), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('url')
    )
    op.create_table('sources',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('bias', sa.Integer(), nullable=True),
    sa.Column('allSidesURL', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('socialID', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('test', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('socialID')
    )
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('visits',
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('userID', sa.String(length=128), nullable=False),
    sa.Column('timeIn', sa.DateTime(), nullable=False),
    sa.Column('timeOut', sa.DateTime(), nullable=True),
    sa.Column('lastActiveTime', sa.DateTime(), nullable=True),
    sa.Column('state', sa.String(length=32), nullable=True),
    sa.Column('timeSpent', sa.Float(), nullable=True),
    sa.Column('receivedSuggestions', sa.Boolean(), nullable=True),
    sa.Column('clickedSuggestion', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('userID', 'timeIn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visits')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_table('users')
    op.drop_table('sources')
    op.drop_table('articles')
    # ### end Alembic commands ###
