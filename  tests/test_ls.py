from pathlib import Path

import pytest


def test_success_without_hidden(linux_console):
    res = " ".join(linux_console.ls(Path("/home/test/"), hidden=False, detailed=False))
    assert "data1" in res
    assert "data2" in res
    assert ".data3" not in res


def test_success_hidden(linux_console):
    res = " ".join(linux_console.ls(Path("/home/test/"), hidden=True, detailed=False))
    assert "data1" in res
    assert ".data3" in res

def test_success_default(linux_console):
    res = " ".join(linux_console.ls(Path("/home/test/"), hidden=True, detailed=True))
    assert "rwx" not in res or "drwx" not in res or "rx" not in res

def test_success_detailed(linux_console):
    res = " ".join(linux_console.ls(Path("/home/test/"), hidden=True, detailed=True))
    assert "rwx" in res or "drwx" in res or "rx" in res or "drwxr" in res

def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.ls(Path("/home/test/dflsflsfld"), hidden=True, detailed=False)

def test_e_dir(linux_console):
    with pytest.raises(NotADirectoryError):
        linux_console.ls(Path("/home/test/testD.txt"), hidden=True, detailed=False)
