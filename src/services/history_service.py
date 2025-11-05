from shutil import copy2, copytree
from pathlib import Path


class HistoryService:
    def __init__(self):
        project_root = Path(__file__).parent.parent.parent

        self.stack = []
        self.history_file = project_root / ".history"
        self.trash_dir = project_root / ".trash"

        self.history_file.touch(exist_ok=True)
        self.trash_dir.mkdir(parents=True, exist_ok=True)

    def add(self, command: str) -> None:
        """
        Функция добавляет команду в историю в файле .history.
        Чтобы поддерживать индексацию, все время проверяем кол-во строк файла .history.
        Затем добавляем в файл команду.
        """
        with open(self.history_file, "r", encoding="utf-8") as f:
            strings = f.readlines()
        command_id = len(strings) + 1

        with open(self.history_file, "a", encoding="utf-8") as f:
            f.writelines(f"{command_id} {command}\n")

    def get(self, length: int) -> list[str]:
        """
        Функция занимается выводом из файла .history.
        Считываем строки -> Выводим в зависимости от длины и в указанной последовательности.
        """
        if length == 0:
            return []

        with open(self.history_file, "r", encoding="utf-8") as f:
            strings = f.readlines()

        strings = strings[::-1]

        if length > len(strings) or length == -1:
            return strings
        return strings[:length]

    def add_undo(
            self,
            command_type: str,
            src: str,
            destination: str = None,
            backup: str = None,
            r: bool = True
    ) -> None:
        """Добавление определенной команды в стек с нужными параметрами."""
        self.stack.append({
            "type": command_type,
            "source": src,
            "destination": destination,
            "backup_path": backup,
            "recursive": r,
        })

    def get_undo(self) -> dict | None:
        """Взятие последней отменяемой функции из стека."""
        if self.stack:
            return self.stack.pop()
        return None

    def backup(self, path: Path):
        """
        Реализация занесения файла в .trash перед удалением с помощью copy2 и copytree от shutil в зависимости от типа.
        Если файл в корзине подобный существует - прикручиваем к имени цифры.
        """
        backup_path = self.trash_dir / path.name

        counter = 1
        while backup_path.exists():
            backup_path = self.trash_dir / f"{backup_path.name}_{counter}"
            counter += 1

        if path.exists():
            if path.is_file():
                copy2(path, backup_path)
            else:
                copytree(path, backup_path)

        return backup_path
