from pathlib import Path

import pytest

from enums.file_mode import FileReadMode


def test_success_default(linux_console):
    res = linux_console.cat("/home/test/testD.txt")
    assert res == "TEST D"


def test_success_string(linux_console):
    res = linux_console.cat(Path("/home/test/testD.txt"), mode=FileReadMode.string)
    assert res == "TEST D"


def test_success_bytes(linux_console):
    res = linux_console.cat(Path("/home/test/testD.txt"), mode=FileReadMode.bytes)
    assert res == b"TEST D"


def test_success_empty(linux_console):
    res = linux_console.cat(Path("/home/test/data1/empty.txt"), mode=FileReadMode.string)
    assert res == ""

def test_success_symlink(linux_console, fake_system):
    res = linux_console.cat(Path("/home/link.txt"))
    assert res == "GOOD SYMLINK"

def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.cat("/home/test/file.txt")

def test_e_empty(linux_console):
    with pytest.raises(IsADirectoryError):
        linux_console.cat("")

def test_e_dir(linux_console):
    with pytest.raises(IsADirectoryError):
        linux_console.cat("/home/test/data1")


def test_e_not_permission(linux_console, fake_system):
    with pytest.raises(PermissionError):
        linux_console.cat("no_access.txt")



