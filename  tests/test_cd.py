from pathlib import Path

import pytest

def test_success_root(linux_console):
    linux_console.cd(Path("/"))
    assert linux_console.current_path == Path("/")

def test_success_cur_dir(linux_console):
    before_path = linux_console.current_path
    linux_console.cd(Path("."))
    assert linux_console.current_path == before_path

def test_success_parent_dir(linux_console):
    before_path = linux_console.current_path
    linux_console.cd(Path(".."))
    assert linux_console.current_path == before_path.parent

def test_success_absolute(linux_console):
    linux_console.cd("/home/test/data1")
    assert linux_console.current_path == Path("/home/test/data1")

def test_success_relative_1(linux_console):
    linux_console.cd("data1")
    assert linux_console.current_path == Path("/home/test/data1")

def test_success_relative_2(linux_console):
    linux_console.cd("data1")
    linux_console.cd("../data2")
    assert linux_console.current_path == Path("/home/test/data2")

def test_success_empty(linux_console):
    linux_console.cd("")
    assert linux_console.current_path == Path("/home/test/")

def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.cd("/home/home/home/home")

def test_e_not_dir(linux_console):
    with pytest.raises(NotADirectoryError):
        linux_console.cd("/home/test/testD.txt")
