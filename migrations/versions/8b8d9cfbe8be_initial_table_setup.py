"""initial table setup

Revision ID: 8b8d9cfbe8be
Revises: 
Create Date: 2024-11-15 12:21:10.911226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b8d9cfbe8be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('band',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=25), nullable=False),
    sa.Column('band_picture', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('band', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_band_name'), ['name'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('art', sa.String(length=150), nullable=True),
    sa.Column('release_type', sa.String(length=10), nullable=False),
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['band_id'], ['band.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('release', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_release_band_id'), ['band_id'], unique=False)

    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('review_text', sa.String(length=500), nullable=False),
    sa.Column('release_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['release_id'], ['release.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_review_release_id'), ['release_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_review_user_id'), ['user_id'], unique=False)

    op.create_table('track',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('lyrics', sa.String(length=256), nullable=True),
    sa.Column('release_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['release_id'], ['release.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('track', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_track_release_id'), ['release_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('track', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_track_release_id'))

    op.drop_table('track')
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_review_user_id'))
        batch_op.drop_index(batch_op.f('ix_review_release_id'))

    op.drop_table('review')
    with op.batch_alter_table('release', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_release_band_id'))

    op.drop_table('release')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('band', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_band_name'))

    op.drop_table('band')
    # ### end Alembic commands ###
