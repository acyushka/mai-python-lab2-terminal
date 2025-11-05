from pathlib import Path

import pytest

def test_make_success(linux_console):
    linux_console.archive("zip", "/home/test/data1", "/home/test/archive.zip")
    assert Path("/home/test/archive.zip").exists()

def test_make_empty_dir(linux_console):
    linux_console.archive("zip", "/home/test/data2", "/home/test/empty.zip")
    assert Path("/home/test/empty.zip").exists()

def test_make_e_notfound(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.archive("zip", "nononono", "archive.zip")


def test_make_e_not_dir(linux_console):
    with pytest.raises(NotADirectoryError):
        linux_console.archive("zip", "/home/test/testD.txt", "/home/test/archive.zip")

def test_make_e_invalid_format(linux_console):
    with pytest.raises(OSError, match="неправильный или сломанный"):
        linux_console.archive("FAIL", "/home/test/data1", "/home/test/archive.FAIL")

def test_unpack_success(linux_console, fake_system):
    linux_console.archive("zip", "/home/test/data1", "/home/archive.zip")
    linux_console.unpack_archive("zip", "/home/archive.zip")
    assert Path("/home/test/test1.txt").exists()
    assert Path("/home/test/test2.txt").exists()
    assert Path("/home/test/empty.txt").exists()

def test_unpack_nonexistent_archive(linux_console):
    with pytest.raises(FileNotFoundError):
        linux_console.unpack_archive("zip", "nononono.zip")

def test_unpack_e_not_archive(linux_console):
    with pytest.raises(NotADirectoryError):
        linux_console.unpack_archive("zip", "/home/test/data1")

def test_unpack_e_invalid_format(linux_console, fake_system):
    fake_system.create_file("invalid_format.FAIL")
    with pytest.raises(OSError, match="неправильный или сломанный формат архива"):
        linux_console.unpack_archive("zip", "invalid_format.FAIL")
