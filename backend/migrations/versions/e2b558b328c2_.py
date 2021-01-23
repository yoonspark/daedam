"""empty message

Revision ID: e2b558b328c2
Revises:
Create Date: 2021-01-23 12:40:31.498322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2b558b328c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Call',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(length=1000), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Offer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=True),
        sa.Column('contents', sa.String(), nullable=True),
        sa.Column('event_time', sa.DateTime(), nullable=True),
        sa.Column('finalized', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Panelist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('city', sa.String(length=120), nullable=True),
        sa.Column('state', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=120), nullable=True),
        sa.Column('image_link', sa.String(length=500), nullable=True),
        sa.Column('facebook_link', sa.String(length=120), nullable=True),
        sa.Column('website', sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Topic',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('call_topic',
        sa.Column('call_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['call_id'], ['Call.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['Topic.id'], ),
        sa.PrimaryKeyConstraint('call_id', 'topic_id')
    )
    op.create_table('offer_panelist',
        sa.Column('offer_id', sa.Integer(), nullable=False),
        sa.Column('panelist_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['offer_id'], ['Offer.id'], ),
        sa.ForeignKeyConstraint(['panelist_id'], ['Panelist.id'], ),
        sa.PrimaryKeyConstraint('offer_id', 'panelist_id')
    )
    op.create_table('offer_topic',
        sa.Column('offer_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['offer_id'], ['Offer.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['Topic.id'], ),
        sa.PrimaryKeyConstraint('offer_id', 'topic_id')
    )
    op.create_table('panelist_topic',
        sa.Column('panelist_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['panelist_id'], ['Panelist.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['Topic.id'], ),
        sa.PrimaryKeyConstraint('panelist_id', 'topic_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('panelist_topic')
    op.drop_table('offer_topic')
    op.drop_table('offer_panelist')
    op.drop_table('call_topic')
    op.drop_table('Topic')
    op.drop_table('Panelist')
    op.drop_table('Offer')
    op.drop_table('Call')
    # ### end Alembic commands ###
