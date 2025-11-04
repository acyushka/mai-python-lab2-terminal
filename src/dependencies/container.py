from dataclasses import dataclass

from services.history_service import HistoryService
from src.services.linux_console import LinuxConsoleService

@dataclass
class Container:
    console_service: LinuxConsoleService
    history_service: HistoryService
