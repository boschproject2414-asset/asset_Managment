"""initial schema

Revision ID: 20261201_0001
Revises:
Create Date: 2026-12-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20261201_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=180), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('ASSET_INCHARGE', 'INTERNAL_TEAM', 'EXTERNAL_DEPARTMENT', name='user_role'), nullable=False),
        sa.Column('department', sa.String(length=120), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('email'),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table(
        'tools',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tool_code', sa.String(length=50), nullable=False),
        sa.Column('tool_name', sa.String(length=160), nullable=False),
        sa.Column('category', sa.String(length=120), nullable=False),
        sa.Column('location', sa.String(length=120), nullable=False),
        sa.Column('ownership', sa.Enum('INTERNAL', 'EXTERNAL', 'VENDOR', name='tool_ownership'), nullable=False),
        sa.Column('status', sa.Enum('AVAILABLE', 'ISSUED', 'MAINTENANCE', 'CALIBRATION', name='tool_status'), nullable=False),
        sa.Column('calibration_due_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('tool_code'),
    )
    op.create_index('ix_tools_tool_code', 'tools', ['tool_code'])
    op.create_index('ix_tools_tool_name', 'tools', ['tool_name'])
    op.create_index('ix_tools_status_category', 'tools', ['status', 'category'])

    op.create_table(
        'trolleys',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('trolley_code', sa.String(length=50), nullable=False),
        sa.Column('project', sa.String(length=120), nullable=False),
        sa.Column('department', sa.String(length=120), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', name='trolley_status'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('trolley_code'),
    )
    op.create_index('ix_trolleys_trolley_code', 'trolleys', ['trolley_code'])

    op.create_table(
        'trolley_tools',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('trolley_id', sa.Integer(), sa.ForeignKey('trolleys.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tool_id', sa.Integer(), sa.ForeignKey('tools.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('trolley_id', 'tool_id', name='uq_trolley_tools_trolley_tool'),
    )

    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tool_id', sa.Integer(), sa.ForeignKey('tools.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('requested_by_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('user_role', sa.Enum('ASSET_INCHARGE', 'INTERNAL_TEAM', 'EXTERNAL_DEPARTMENT', name='ticket_user_role'), nullable=False),
        sa.Column('department', sa.String(length=120), nullable=False),
        sa.Column('project', sa.String(length=120), nullable=True),
        sa.Column('trolley_id', sa.Integer(), sa.ForeignKey('trolleys.id', ondelete='SET NULL'), nullable=True),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('request_date', sa.Date(), nullable=False),
        sa.Column('expected_return_date', sa.Date(), nullable=True),
        sa.Column('approval_status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status'), nullable=False),
        sa.Column('issue_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('return_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('issued_by_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.Enum('REQUESTED', 'ISSUED', 'RETURNED', 'CLOSED', name='ticket_status'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_tickets_approval_status_request_date', 'tickets', ['approval_status', 'request_date'])

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('action', sa.String(length=120), nullable=False),
        sa.Column('actor_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('tool_id', sa.Integer(), sa.ForeignKey('tools.id', ondelete='SET NULL'), nullable=True),
        sa.Column('ticket_id', sa.Integer(), sa.ForeignKey('tickets.id', ondelete='SET NULL'), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_index('ix_tickets_approval_status_request_date', table_name='tickets')
    op.drop_table('tickets')
    op.drop_table('trolley_tools')
    op.drop_index('ix_trolleys_trolley_code', table_name='trolleys')
    op.drop_table('trolleys')
    op.drop_index('ix_tools_status_category', table_name='tools')
    op.drop_index('ix_tools_tool_name', table_name='tools')
    op.drop_index('ix_tools_tool_code', table_name='tools')
    op.drop_table('tools')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
