from datetime import date, timedelta

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.enums import ApprovalStatus, TicketStatus, ToolOwnership, ToolStatus, TrolleyStatus, UserRole
from app.models.ticket import Ticket
from app.models.tool import Tool
from app.models.trolley import Trolley
from app.models.trolley_tool import TrolleyTool
from app.models.user import User


def run() -> None:
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print('Seed already exists')
            return

        admin = User(
            full_name='Asset Incharge Admin',
            email='admin@bosch.local',
            hashed_password=get_password_hash('Admin@123'),
            role=UserRole.ASSET_INCHARGE,
            department='Asset Control',
        )
        internal = User(
            full_name='Internal Engineer',
            email='internal@bosch.local',
            hashed_password=get_password_hash('Internal@123'),
            role=UserRole.INTERNAL_TEAM,
            department='Engine Testing',
        )
        external = User(
            full_name='External Calibration Lead',
            email='external@bosch.local',
            hashed_password=get_password_hash('External@123'),
            role=UserRole.EXTERNAL_DEPARTMENT,
            department='Calibration Dept',
        )
        db.add_all([admin, internal, external])

        tools = [
            Tool(tool_code='TL-1001', tool_name='Oscilloscope Tek', category='Instrumentation', location='Lab-A', ownership=ToolOwnership.INTERNAL, status=ToolStatus.AVAILABLE, calibration_due_date=date.today()+timedelta(days=20)),
            Tool(tool_code='TL-1002', tool_name='Multimeter Fluke', category='Electrical', location='Lab-A', ownership=ToolOwnership.INTERNAL, status=ToolStatus.AVAILABLE, calibration_due_date=date.today()-timedelta(days=1)),
            Tool(tool_code='TL-1003', tool_name='Torque Wrench', category='Mechanical', location='Tool-Rack-3', ownership=ToolOwnership.VENDOR, status=ToolStatus.MAINTENANCE),
            Tool(tool_code='TL-1004', tool_name='BNC Cable Kit', category='Cables', location='Rack-C', ownership=ToolOwnership.EXTERNAL, status=ToolStatus.AVAILABLE),
        ]
        db.add_all(tools)

        trolleys = [
            Trolley(trolley_code='TR-001', project='Project Alpha', department='Engine Testing', status=TrolleyStatus.ACTIVE),
            Trolley(trolley_code='TR-002', project='Project Beta', department='Dyno', status=TrolleyStatus.ACTIVE),
        ]
        db.add_all(trolleys)
        db.flush()

        db.add_all([
            TrolleyTool(trolley_id=trolleys[0].id, tool_id=tools[0].id),
            TrolleyTool(trolley_id=trolleys[0].id, tool_id=tools[1].id),
        ])

        ticket = Ticket(
            tool_id=tools[0].id,
            requested_by_id=internal.id,
            user_role=internal.role,
            department=internal.department,
            project='Project Alpha',
            trolley_id=trolleys[0].id,
            reason='Engine ignition waveform validation',
            request_date=date.today(),
            expected_return_date=date.today()+timedelta(days=3),
            approval_status=ApprovalStatus.PENDING,
            status=TicketStatus.REQUESTED,
        )
        db.add(ticket)
        db.commit()
        print('Seed complete')
    finally:
        db.close()


if __name__ == '__main__':
    run()
