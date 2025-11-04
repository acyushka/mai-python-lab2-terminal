import os
import re
from os import PathLike
import shutil
from pathlib import Path
from typing import Literal

from enums.constants import BINARY
from src.enums.file_mode import FileReadMode
from src.utils.ls import default_ls, detailed_ls


class LinuxConsoleService:
    def __init__(self):
        self.current_path = Path.cwd()
        pass

    def ls(self, path: PathLike[str] | str, hidden: bool, detailed: bool) -> list[str]:
        if path is None:
            path = self.current_path
        else:
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"ls: '{path}': Каталог не существует")
        if not path.is_dir():
            raise NotADirectoryError(f"grep: '{path}': Это не каталог")

        items = [item.name for item in path.iterdir()]
        if not hidden:
            items = [item for item in items if not item.startswith(".")]
        items.sort()

        if detailed:
            result = detailed_ls(path, items)
        else:
            result = default_ls(items)
        return result

    def cd(self, path: PathLike[str] | str) -> None:
        match path:
            case "/":
                path = Path("/")
            case ".":
                path = self.current_path
            case "..":
                path = self.current_path.parent
            case _:
                path_string = str(path)
                if path_string.startswith("~"):
                    path = os.path.expanduser(path_string)

                path = Path(path)

                if not path.is_absolute():
                    path = (self.current_path / path).resolve()

        if not path.exists():
            raise FileNotFoundError(f"cd: '{path}': Каталог не существует")
        if not path.is_dir():
            raise NotADirectoryError(f"cd:'{path}'; Это не каталог")

        self.current_path = path
        try:
            os.chdir(path)
        except Exception as e:
            raise OSError(f"Ошибка: {e}")

    def cat(
            self,
            file: PathLike[str] | str,
            mode: Literal[FileReadMode.string, FileReadMode.bytes] = FileReadMode.string,
    ) -> str | bytes:
        path = Path(file)
        if not path.exists(follow_symlinks=True):
            raise FileNotFoundError(f"cat: '{path}': Файл не существует")
        if not path.is_file():
            raise IsADirectoryError(f"cat: '{path}': Это не файл")
        if not os.access(path, os.R_OK):
            raise PermissionError(f"cat: {path}; Отказано в доступе")

        try:
            match mode:
                case FileReadMode.string:
                    return path.read_text("utf-8")
                case FileReadMode.bytes:
                    return path.read_bytes()
        except Exception as e:
            raise OSError(f"Ошибка: {e}")

    def cp(
            self,
            src: PathLike[str] | str,
            dst: PathLike[str] | str,
            recursive: bool,
    ):
        src_path = Path(src)
        dst_path = Path(dst)

        if not src_path.exists():
            raise FileNotFoundError(f"cp: '{src}': Файл не существует")
        if src_path.is_dir() and dst_path.exists() and dst_path.is_file():
            raise IsADirectoryError("cp: невозможно перезаписать некаталоговый объект каталогом")

        try:
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
            elif src_path.is_dir():
                if recursive:
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    raise IsADirectoryError(f"cp: не указан -r; пропускается каталог '{src_path}'")
            else:
                raise ValueError(f"cp: невозможно скопировать '{src}'; Неподдерживаемый тип файла")
        except PermissionError:
            raise PermissionError("cp: Отказано в доступе")

    def mv(self, src: PathLike[str] | str, dst: PathLike[str] | str) -> None:
        src_path = Path(src)
        dst_path = Path(dst)

        if not src_path.exists():
            raise FileNotFoundError(f"mv: '{src}': Файл не существует")

        try:
            shutil.move(src_path, dst_path)
        except PermissionError:
            raise PermissionError("mv: Отказано в доступе")

    def rm(self, path: PathLike[str] | str, recursive: bool) -> None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"mv: '{path}': Файл не существует")
        if str(path) in ("..", "/") or path.resolve() == Path("/"):
            raise PermissionError(f"rm: невозможно удалить '{path}'; Отказано в доступе")
        try:
            if path.is_file():
                os.remove(path)
            elif path.is_dir():
                if recursive:
                    shutil.rmtree(path)
                else:
                    raise IsADirectoryError(f"rm: невозможно удалить '{path}'; Это каталог")
            else:
                raise TypeError(f"rm: невозможно удалить '{path}'; Неизвестный тип файла")
        except PermissionError:
            raise PermissionError(f"rm: невозможно удалить '{path}'; Отказано в доступе")

    # ФУНКЦИИ for Medium level:

    def archive(self, format: str, folder: PathLike[str] | str, name: PathLike[str] | str) -> None:
        base_dir = Path(folder)
        archive_path = Path(name)

        if not base_dir.exists():
            raise FileNotFoundError(f"{format}: '{folder}': Каталог не существует")
        if not base_dir.is_dir():
            raise NotADirectoryError(f"{format}: '{folder}': Это не каталог")

        try:
            base_name = str(archive_path.with_suffix(''))
            shutil.make_archive(base_name, format, base_dir)
        except PermissionError:
            raise PermissionError(f"{format}: Отказано в доступе")
        except (ValueError, shutil.ReadError):
            raise OSError(f"{format}: неправильный или сломанный формат архива")
        except Exception as e:
            raise OSError(f"Ошибка: {e}")

    def unpack_archive(self, format: str, name: PathLike[str] | str) -> None:
        filename = Path(name)

        if not filename.exists():
            raise FileNotFoundError(f"{format}: '{name}': Архив не существует")
        if not filename.is_file():
            raise NotADirectoryError(f"{format}: '{name}': Это не архив")

        try:
            shutil.unpack_archive(filename, self.current_path)
        except PermissionError:
            raise PermissionError(f"{format}: Отказано в доступе")
        except (ValueError, shutil.ReadError):
            raise OSError(f"{format}: неправильный или сломанный формат архива")
        except Exception as e:
            raise OSError(f"Ошибка: {e}")

    def grep(self, pattern: str, path: PathLike[str] | str, r: bool, i: bool) -> list[str]:
        path = Path(path)
        ignore_flag = 0
        if i: ignore_flag = re.IGNORECASE

        if not path.exists():
            raise FileNotFoundError(f"grep: '{path}': Файл не существует")

        try:
            pattern = re.compile(pattern, ignore_flag)
        except:
            raise ValueError("grep: некорректный формат паттерна")

        result = []

        if path.is_file():
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for i, string in enumerate(f, 1):
                    if pattern.search(string):
                        result.append(f"{path}:{i}:{string}")

        elif path.is_dir():
            if r:
                for dirpath, _, filenames in os.walk(path):
                    for file in filenames:
                        file_path = Path(dirpath) / file

                        if file_path.suffix in BINARY:
                            result.append(f"grep: {file_path.relative_to(path)}: двоичный файл совпадает\n")
                            continue

                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                for i, string in enumerate(f, 1):
                                    if pattern.search(string):
                                        relative_path = file_path.relative_to(path)
                                        result.append(f"{relative_path}:{i}:{string}")
                        except OSError:
                            continue
            else:
                raise IsADirectoryError(f"grep: '{path}': Это каталог")
        else:
            raise ValueError(f"grep: '{path}': Не является файлом или каталогом")

        return result
