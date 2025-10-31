import sys
from os import PathLike
from pathlib import Path
import typer
from typer import Typer, Context
from src.dependencies.container import Container
from src.services.linux_console import LinuxConsoleService

app = Typer()


def get_container(ctx: Context) -> Container:
    container = ctx.obj
    if not isinstance(container, Container):
        raise RuntimeError("DI Container is not initialized")
    return container


@app.callback()
def main(ctx: Context) -> None:
    # logger
    ctx.obj = Container(console_service=LinuxConsoleService())


@app.command()
def ls(
        ctx: Context,
        path: Path = typer.Argument(
            None, exists=False, readable=False)
) -> None:
    if path is None:
        path = Path.cwd()
    try:
        container = get_container(ctx)
        result = container.console_service.ls(path)
        sys.stdout.writelines(result)
    except OSError as e:
        typer.echo(str(e), err=True)


@app.command()
def rm(
        ctx: Context,
        path: Path = typer.Argument(None, help="Удалить папки или файлы из каталога"),
        recursive: bool = typer.Option(False, "-r", "-R", help="Необходимый флаг для удаления папок (рекурсивно)"),
) -> None:
    if path is None:
        typer.echo("rm: пропущен операнд")
        return

    try:
        container = get_container(ctx)

        if recursive and path.is_dir():
            if not typer.confirm(f"Вы уверены, что хотите удалить каталог '{path}': [y/n]"):
                typer.echo("Операция отменена")
                return

        container.console_service.rm(path, recursive)

    except OSError as e:
        typer.echo(str(e), err=True)


if __name__ == "__main__":
    app()
