import sys
from pathlib import Path
from loguru import logger
from typer import Typer, Context
from src.dependencies.container import Container
from src.enums.file_mode import FileReadMode
from src.services.linux_console import LinuxConsoleService
import click
import typer
from click_shell import make_click_shell

from utils.log_shell import log_shell
from utils.validators import validate_archive

app = Typer(
    no_args_is_help=False,
)


@click.group()
@click.pass_context
def my_app(ctx):
    pass


def get_container(ctx: Context) -> Container:
    container = ctx.obj
    if not isinstance(container, Container):
        raise RuntimeError("DI Container is not initialized")
    return container


@app.callback()
def main(ctx: Context) -> None:
    logger.remove()
    logger.add("shell.log", format="[{time:YYYY-MM-DD HH:mm:ss}] {message}", colorize=True)

    ctx.obj = Container(console_service=LinuxConsoleService())


@app.command()
def ls(
        ctx: Context,
        path: Path = typer.Argument(
            None, exists=False, readable=False),
        hidden: bool = typer.Option(False, "-a", help="Флаг для отображения скрытых файлов"),
        detailed: bool = typer.Option(False, "-l", help="Флаг для более подробного и структурированного вывода команды")
) -> None:
    try:
        container = get_container(ctx)
        result = container.console_service.ls(path, hidden, detailed)
        sys.stdout.writelines(result)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


@app.command()
def cd(
        ctx: Context,
        path: Path = typer.Argument(None, help="Переместиться в указанный каталог")
):
    if path in (None, "~"):
        path = Path.home()

    try:
        container: Container = get_container(ctx)
        container.console_service.cd(path)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


@app.command()
def cat(
        ctx: Context,
        file: Path = typer.Argument(
            ..., exists=False, readable=False, help="Вывести содержимое файла"
        ),
        mode: bool = typer.Option(False, "-b", "--bytes", help="Прочитать файл как слайс байтов")
):
    try:
        container: Container = get_container(ctx)
        mode = FileReadMode.bytes if mode else FileReadMode.string
        data = container.console_service.cat(file, mode)
        if isinstance(data, str):
            sys.stdout.write(data)
        else:
            sys.stdout.buffer.write(data)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


@app.command()
def cp(
        ctx: Context,
        source: Path = typer.Argument(None, help="Источник копирования"),
        destination: Path = typer.Argument(None, help="Путь назначения"),
        recursive: bool = typer.Option(False, "-r", "-R", help="Необходимый для рекурсивного копирования флаг"),
) -> None:
    if source is None:
        logger.error("ERROR: cp: пропущен операнд, задающий файл")
        typer.echo("cp: пропущен операнд, задающий файл")
        return
    if destination is None:
        logger.error("ERROR: cp: пропущен операнд, задающий целевой файл")
        typer.echo("cp: пропущен операнд, задающий целевой файл")
        return

    try:
        container: Container = get_container(ctx)
        container.console_service.cp(source, destination, recursive)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


@app.command()
def mv(
        ctx: Context,
        source: Path = typer.Argument(None, help="Перемещаемый источник"),
        destination: Path = typer.Argument(None, help="Путь назначения"),
) -> None:
    if source is None:
        logger.error("ERROR: mv: пропущен операнд, задающий файл")
        typer.echo("mv: пропущен операнд, задающий файл")
        return
    if destination is None:
        logger.error("ERROR: mv: пропущен операнд, задающий целевой файл")
        typer.echo("mv: пропущен операнд, задающий целевой файл")
        return

    try:
        container: Container = get_container(ctx)
        container.console_service.mv(source, destination)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


@app.command()
def rm(
        ctx: Context,
        path: Path = typer.Argument(None, help="Удалить папки или файлы из каталога"),
        recursive: bool = typer.Option(False, "-r", "-R", help="Необходимый флаг для удаления папок (рекурсивно)"),
) -> None:
    if path is None:
        logger.error("ERROR: rm: пропущен операнд")
        typer.echo("rm: пропущен операнд")
        return

    try:
        container = get_container(ctx)

        if recursive and path.is_dir():
            if not typer.confirm(f"Вы уверены, что хотите удалить каталог '{path}': [y/n]"):
                typer.echo("Операция отменена")
                return

        container.console_service.rm(path, recursive)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)


# ФУНКЦИИ for Medium level:

@app.command()
def zip(
        ctx: Context,
        folder: Path = typer.Argument(None, help="Каталог, который хотите заархивировать"),
        filename: Path = typer.Argument(None, help="Имя архивируемого каталога"),
):
    validate_archive("zip", filename, folder)

    try:
        container = get_container(ctx)
        container.console_service.archive("zip", folder, filename)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)

@app.command()
def unzip(
        ctx: Context,
        filename: Path = typer.Argument(None, help="Имя zip-архива, который хотите разархивировать"),
):
    validate_archive("zip", filename, "pass")

    try:
        container = get_container(ctx)
        container.console_service.unpack_archive("zip", filename)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)

@app.command()
def tar(
        ctx: Context,
        folder: Path = typer.Argument(None, help="Каталог, который хотите заархивировать"),
        filename: Path = typer.Argument(None, help="Имя архивируемого каталога"),
):
    validate_archive("tar", filename, folder)

    try:
        container = get_container(ctx)
        container.console_service.archive("tar" ,folder, filename)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)

@app.command()
def untar(
        ctx: Context,
        filename: Path = typer.Argument(None, help="Имя tar-архива, который хотите разархивировать"),
):
    validate_archive("tar", filename, "pass")

    try:
        container = get_container(ctx)
        container.console_service.unpack_archive("tar", filename)
        logger.success("SUCCESS")
    except OSError as e:
        logger.error(f"ERROR: {str(e)}")
        typer.echo(str(e), err=True)

@app.callback(invoke_without_command=True)
def base(ctx: typer.Context):
    logger.remove()
    logger.add("shell.log", format="[{time:YYYY-MM-DD HH:mm:ss}] {message}", colorize=True)

    ctx.obj = Container(console_service=LinuxConsoleService())

    if ctx.invoked_subcommand is None:
        shell = make_click_shell(ctx, prompt=f'{ctx.obj.console_service.current_path} ', intro='...Терминал запущен...')
        shell.precmd = log_shell
        shell.cmdloop()
        typer.Exit(0)


if __name__ == "__main__":
    app()
