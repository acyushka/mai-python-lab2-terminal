from pathlib import Path

import pytest


def test_success_file(linux_console):
    linux_console.rm("/home/test/testD.txt", False)
    assert not Path("/home/test/testD.txt").exists()


def test_success_dir_recursive(linux_console):
    linux_console.rm("/home/test/data1", True)
    assert not Path("/home/test/data1").exists()
    assert not Path("/home/test/data1/test1.txt").exists()
    assert not Path("/home/test/data1/test2.txt").exists()


def test_success_empty_dir_recursive(linux_console):
    linux_console.rm("/home/test/data2", True)
    assert not Path("/home/test/data2").exists()


def test_success_hidden_file(linux_console):
    linux_console.rm("/home/test/.data3/.secret.txt", False)
    assert not Path("/home/test/.data3/.secret.txt").exists()


def test_success_hidden_dir(linux_console):
    linux_console.rm("/home/test/.data3", True)
    assert not Path("/home/test/.data3").exists()

def test_rm_directory_without_recursive(linux_console):
    with pytest.raises(IsADirectoryError):
        linux_console.rm("/home/test/data1", False)

def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.rm("nononononono.txt", False)

def test_e_root(linux_console):
    with pytest.raises(PermissionError):
        linux_console.rm("/", True)

def test_e_parent_directory(linux_console):
    with pytest.raises(PermissionError):
        linux_console.rm("..", True)

def test_e_current_directory_dot(linux_console):
    with pytest.raises(PermissionError):
        linux_console.rm(".", True)


def test_rm_unknown_file_type_simple(linux_console, monkeypatch):
    monkeypatch.setattr('src.services.linux_console.Path.is_file', lambda self: False)
    monkeypatch.setattr('src.services.linux_console.Path.is_dir', lambda self: False)
    with pytest.raises(TypeError):
        linux_console.rm("/home/test/testD.txt", False)
