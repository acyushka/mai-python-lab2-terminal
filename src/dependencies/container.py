from dataclasses import dataclass
from src.services.linux_console import LinuxConsoleService

@dataclass
class Container:
    console_service: LinuxConsoleService