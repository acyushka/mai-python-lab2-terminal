import os
from os import PathLike
import shutil
from pathlib import Path


class LinuxConsoleService:
    def __init__(self):
        pass
        # self.logger = Logger

    def ls(self, path: PathLike[str] | str) -> list[str]:
        path = Path(path)
        if not path.exists():
            # log
            raise FileNotFoundError(path)
        if not path.is_dir():
            # log
            raise NotADirectoryError(path)
        # log
        return [obj.name + "\n" for obj in path.iterdir()]

    def rm(self, path: PathLike[str] | str, recursive: bool) -> None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        try:
            if path.is_file():
                os.remove(path)
            elif path.is_dir():
                if recursive:
                    shutil.rmtree(path)
                else:
                    raise IsADirectoryError(f"rm: невозможно удалить '{path}': Это каталог")
            else:
                raise TypeError(f"rm: невозможно удалить '{path}': Неизвестный тип файла")
        except PermissionError:
            raise PermissionError(f"rm: невозможно удалить '{path}': Отказано в доступе")
