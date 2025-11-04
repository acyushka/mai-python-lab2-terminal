from datetime import datetime
import os
from os import PathLike
import stat


def default_ls(items: list[str]) -> list[str]:
    if not items:
        return ["\n"]

    k = (len(items) // 6) + 1
    column_width = max(len(item) for item in items)
    strings = []

    for i in range(0, len(items), k):
        string = "".join(f"{item:<{column_width}}" for item in items[i:i+k])
        strings.append(string + "\n")

    return strings

def detailed_ls(path: PathLike[str] | str, items: list[str]) -> list[str]:
    strings = []
    for filename in items:
        item_path = os.path.join(path, filename)
        item_stat = os.stat(item_path)

        permissions = stat.filemode(item_stat.st_mode)
        size = item_stat.st_size
        time = datetime.fromtimestamp(item_stat.st_mtime).strftime("%b %d %H:%M")

        strings.append(f"{permissions} {size:>8} {time} {filename} \n")

    return strings
