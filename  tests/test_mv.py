from pathlib import Path

import pytest


def test_success_file(linux_console):
    linux_console.mv("/home/test/testD.txt", "/home/test/moved.txt")
    assert not Path("/home/test/testD.txt").exists()
    assert Path("/home/test/moved.txt").exists()
    assert Path("/home/test/moved.txt").read_text() == "TEST D"


def test_success_file_to_dir(linux_console):
    linux_console.mv("/home/test/testD.txt", "/home/test/data1")
    assert not Path("/home/test/testD.txt").exists()
    assert Path("/home/test/data1/testD.txt").exists()


def test_success_dir(linux_console):
    linux_console.mv("/home/test/data1", "/home/test/data1_moved")
    assert not Path("/home/test/data1").exists()
    assert Path("/home/test/data1_moved").exists()
    assert Path("/home/test/data1_moved/test1.txt").exists()


def test_success_rename_file(linux_console):
    linux_console.mv("/home/test/testD.txt", "/home/test/renamed.txt")
    assert not Path("/home/test/testD.txt").exists()
    assert Path("/home/test/renamed.txt").exists()


def test_success_rename_dir(linux_console):
    linux_console.mv("/home/test/data1", "/home/test/renamed_data")
    assert not Path("/home/test/data1").exists()
    assert Path("/home/test/renamed_data").exists()


def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.mv("nononono.txt", "moved.txt")


def test_e_permission(linux_console, fake_system):
    fake_system.create_dir("/protected")
    fake_system.chmod("/protected", 0o055)
    with pytest.raises(PermissionError):
        linux_console.mv("/home/test/testD.txt", "/protected/move.txt")
