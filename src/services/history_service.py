from shutil import copy2, copytree
from pathlib import Path


class HistoryService:
    def __init__(self, file: Path = Path(".history")):
        self.stack = []
        self.history_file = file
        self.trash_dir = Path(".trash")

    def add(self, command: str) -> None:
        with open(self.history_file, "r", encoding="utf-8") as f:
            strings = f.readlines()
        command_id = len(strings) + 1

        with open(self.history_file, "a", encoding="utf-8") as f:
            f.writelines(f"{command_id} {command}\n")

    def get(self, length: int) -> list[str]:
        if length == 0:
            return []

        with open(self.history_file, "r", encoding="utf-8") as f:
            strings = f.readlines()

        strings = strings[::-1]

        if length > len(strings):
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
        self.stack.append({
            "type": command_type,
            "source": src,
            "destination": destination,
            "backup_path": backup,
            "recursive": r,
        })

    def get_undo(self) -> dict | None:
        if self.stack:
            return self.stack.pop()
        return None

    def backup(self, path: Path):
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
