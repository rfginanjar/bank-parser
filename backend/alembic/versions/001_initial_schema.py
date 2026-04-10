"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'), nullable=False)
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create accounts table
    op.create_table('accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('account_number', sa.String(100), nullable=False),
        sa.Column('account_name', sa.String(255), nullable=False),
        sa.Column('bank_name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'), nullable=False)
    )
    op.create_index('ix_accounts_user_id', 'accounts', ['user_id'])
    op.create_index('ix_accounts_user_bank', 'accounts', ['user_id', 'bank_name'])

    # Create statements table
    op.create_table('statements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('accounts.id'), nullable=False),
        sa.Column('period_month', sa.Integer, nullable=False),
        sa.Column('period_year', sa.Integer, nullable=False),
        sa.Column('file_url', sa.String, nullable=False),
        sa.Column('file_hash', sa.String(64), nullable=False),
        sa.Column('upload_date', sa.DateTime, server_default=sa.text('now()'), nullable=False),
        sa.Column('status', sa.Enum('pending','processing','extracted','validated','committed', name='statement_status'), nullable=False, server_default='pending')
    )
    op.create_index('ix_statements_account_id', 'statements', ['account_id'])
    op.create_index('ix_statements_status', 'statements', ['status'])
    op.create_unique_constraint('uq_statement_period', 'statements', ['account_id', 'period_month', 'period_year'])

    # Create categories table
    op.create_table('categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('color', sa.String(7), nullable=False),
        sa.Column('is_default', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True, index=True)
    )
    op.create_index('ix_category_user', 'categories', ['user_id'])

    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('statement_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('statements.id'), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('accounts.id'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('mutation_amount', sa.Numeric(12,2), nullable=False),
        sa.Column('type', sa.Enum('Debit','Credit', name='transaction_type'), nullable=False),
        sa.Column('balance', sa.Numeric(12,2), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()'), nullable=False)
    )
    op.create_index('ix_transactions_statement_id', 'transactions', ['statement_id'])
    op.create_index('ix_transactions_account_date_cat_user', 'transactions', ['account_id', 'date', 'category', 'user_id'])
    op.create_index('ix_transactions_date', 'transactions', ['date'])
    op.create_unique_constraint('uq_transaction_unique', 'transactions', ['statement_id', 'date', 'mutation_amount', 'balance'])

    # Create pending_reviews table
    op.create_table('pending_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('statement_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('statements.id'), unique=True, nullable=False),
        sa.Column('raw_transactions', postgresql.JSON, nullable=False),
        sa.Column('validation_token', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False)
    )
    op.create_index('ix_pending_reviews_token', 'pending_reviews', ['validation_token'], unique=True)

    # Insert default categories
    # We'll insert them using op.bulk_insert after table creation
    # But since we're in migration, we can use connection to insert
    # Safer to do in a separate data migration. For simplicity, we could let app seed defaults on startup.
    pass

def downgrade():
    op.drop_table('pending_reviews')
    op.drop_table('transactions')
    op.drop_table('categories')
    op.drop_table('statements')
    op.drop_table('accounts')
    op.drop_table('users')
    # Enums automatically dropped
