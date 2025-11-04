from dataclasses import dataclass

from typer import Context
from services.history_service import HistoryService
from src.services.linux_console import LinuxConsoleService


@dataclass
class Container:
    console_service: LinuxConsoleService
    history_service: HistoryService


def get_container(ctx: Context) -> Container:
    container = ctx.obj
    if not isinstance(container, Container):
        raise RuntimeError("DI Container is not initialized")
    return container
