import enum


class UserRole(str, enum.Enum):
    ASSET_INCHARGE = 'asset_incharge'
    INTERNAL_TEAM = 'internal_team'
    EXTERNAL_DEPARTMENT = 'external_department'


class ToolOwnership(str, enum.Enum):
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    VENDOR = 'vendor'


class ToolStatus(str, enum.Enum):
    AVAILABLE = 'available'
    ISSUED = 'issued'
    MAINTENANCE = 'maintenance'
    CALIBRATION = 'calibration'


class TrolleyStatus(str, enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class ApprovalStatus(str, enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TicketStatus(str, enum.Enum):
    REQUESTED = 'requested'
    ISSUED = 'issued'
    RETURNED = 'returned'
    CLOSED = 'closed'
