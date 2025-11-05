from typer import echo
from loguru import logger


def validate_archive(command, filename, folder):
    """Простая проверка, что обязательные аргументы архивов указаны"""
    if folder is None:
        logger.error(f"ERROR: {command}: пропущен операнд")
        echo(f"{command}: пропущен операнд")
        return
    if filename is None:
        logger.error(f"ERROR: {command}: пропущен операнд")
        echo(f"{command}: пропущен операнд имени {command} архива")
        return
