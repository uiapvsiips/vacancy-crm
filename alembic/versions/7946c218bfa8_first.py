"""first

Revision ID: 7946c218bfa8
Revises: 
Create Date: 2023-02-21 19:18:49.465211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7946c218bfa8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('email_creds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('login', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('pop_server', sa.String(length=120), nullable=False),
    sa.Column('smtp_server', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('templates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation_date', sa.String(length=25), server_default=sa.text("date_trunc('second', now())"), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('position_name', sa.String(length=120), nullable=False),
    sa.Column('company', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=5000), nullable=False),
    sa.Column('contacts_ids', sa.String(length=120), nullable=False),
    sa.Column('comment', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('event_date', sa.String(length=20), server_default=sa.text('now()'), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('due_to_date', sa.String(length=20), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('vacancy')
    op.drop_table('templates')
    op.drop_table('email_creds')
    op.drop_table('user')
    # ### end Alembic commands ###
