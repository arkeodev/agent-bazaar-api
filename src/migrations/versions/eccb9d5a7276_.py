"""empty message

Revision ID: eccb9d5a7276
Revises: 
Create Date: 2024-08-21 12:10:48.822820

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eccb9d5a7276'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop tables in order of dependencies (most dependent first)
    op.drop_table('post')  # Depends on user
    op.drop_table('rate_limit')  # Depends on tier
    op.drop_table('user')
    op.drop_table('tier')

def downgrade() -> None:
    # Create tables in reverse order (dependencies last)
    op.create_table('tier',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tier_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='tier_pkey'),
        sa.UniqueConstraint('name', name='tier_name_key'),
        postgresql_ignore_search_path=False
    )

    op.create_table('user',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
        sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('profile_image_url', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('deleted_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column('tier_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['tier_id'], ['tier.id'], name='user_tier_id_fkey'),
        sa.PrimaryKeyConstraint('id', 'uuid', name='user_pkey'),
        sa.UniqueConstraint('id', name='user_id_key'),
        sa.UniqueConstraint('uuid', name='user_uuid_key')
    )

    op.create_table('rate_limit',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('tier_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('deleted_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['tier_id'], ['tier.id'], name='rate_limit_tier_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='rate_limit_pkey'),
        sa.UniqueConstraint('id', name='rate_limit_id_key')
    )

    op.create_table('post',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('created_by_user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
        sa.Column('text', sa.VARCHAR(length=63206), autoincrement=False, nullable=False),
        sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('media_url', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('deleted_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['user.id'], name='post_created_by_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', 'uuid', name='post_pkey'),
        sa.UniqueConstraint('id', name='post_id_key'),
        sa.UniqueConstraint('uuid', name='post_uuid_key')
    )
