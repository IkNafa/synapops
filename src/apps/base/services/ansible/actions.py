# services/ansible/actions.py
from enum import Enum

class SystemPlaybooks(str, Enum):
    SERVICE = "system/service"
    USER = "system/user"


class Actions:
    SYSTEM = SystemPlaybooks
