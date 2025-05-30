# Import all models to ensure they're registered with SQLAlchemy
from app.models.aircraft import Aircraft, AircraftType
from app.models.audit import AuditLog
from app.models.auth import User, Role, Permission, UserRole, RolePermission

from app.models.dictionary import Dictionary
# from app.models.engineer import Engineer
from app.models.flight import Flight
from app.models.inspection import InspectionRecord, InspectionItem
from app.models.model import Model
from app.models.task import Task
from app.models.terminal import Terminal