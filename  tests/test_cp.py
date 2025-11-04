from pathlib import Path

import pytest

def test_success_file(linux_console):
    linux_console.cp("/home/test/testD.txt", "/home/test/copy.txt", False)
    assert Path("/home/test/copy.txt").exists()
    assert Path("/home/test/copy.txt").read_text() == "TEST D"

def test_success_to_dir(linux_console):
    linux_console.cp("/home/test/testD.txt", "/home/test/data1", False)
    assert Path("/home/test/data1/testD.txt").exists()

def test_success_recursive(linux_console):
    linux_console.cp("/home/test/data1", "/home/test/data11",True)
    assert Path("/home/test/data11").exists()
    assert Path("/home/test/data11/test1.txt").exists()
    assert Path("/home/test/data11/test2.txt").exists()
    assert Path("/home/test/data11/empty.txt").exists()


def test_success_overwrite(linux_console):
    linux_console.cp("/home/test/testD.txt", "/home/test/data1/test2.txt", False)
    assert Path("/home/test/data1/test2.txt").read_text() == "TEST D"

def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.cp("nononono.txt", "copy.txt", False)

def test_e_dir_to_file(linux_console):
    with pytest.raises(IsADirectoryError, match="невозможно перезаписать"):
        linux_console.cp("/home/test/data1", "/home/test/testD.txt", False)

def test_e_without_recursive(linux_console):
    with pytest.raises(IsADirectoryError):
        linux_console.cp("/home/test/data1", "/home/test/data11",False)


def test_e_no_access(linux_console):
    with pytest.raises(PermissionError):
        linux_console.cp("no_access.txt", "copy.txt", False)

