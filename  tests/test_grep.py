from pathlib import Path

import pytest


def test_success_1(linux_console):
    res = linux_console.grep("TEST", Path("/home/test/testD.txt"), False, False)
    assert len(res) > 0
    assert "TEST" in res[0]
    assert "testD.txt" in res[0]

def test_success_no_match(linux_console):
    res = linux_console.grep("LALALALALLALAL", Path("/home/test/testD.txt"), r=False, i=False)
    assert res == []

def test_success_recursive_1(linux_console):
    res = " ".join(linux_console.grep("TEST", "/home/test/data1", r=True, i=False))
    assert len(res) > 0
    assert "test1.txt" in res
    assert "test2.txt" in res

def test_success_recursive_2(linux_console):
    res = " ".join(linux_console.grep("TEST", ".", r=True, i=False))
    assert len(res) >= 3
    assert "test1.txt" in res
    assert "test2.txt" in res
    assert "testD.txt" in res

def test_success_without_ignore(linux_console):
    res = linux_console.grep("test", Path("/home/test/testD.txt"), r=False, i=False)
    assert res == []

def test_success_with_ignore(linux_console):
    res = linux_console.grep("test", Path("/home/test/testD.txt"), r=False, i=True)
    assert len(res) > 0


def test_success_multiple(linux_console, fake_system):
    fake_system.create_file("multi.txt", contents="TEST\nTEST\n")
    result = linux_console.grep("TEST", "multi.txt", r=False, i=False)
    assert len(result) == 2
    
def test_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.grep("pattern", "nononono.txt", r=False, i=False)


def test_e_dir_without_recursive(linux_console):
    with pytest.raises(IsADirectoryError):
        linux_console.grep("pattern", "/home/test/data1", r=False, i=False)


def test_e_invalid_pattern(linux_console):
    with pytest.raises(ValueError):
        linux_console.grep(")t", "/home/test/testD.txt", r=False, i=False)

