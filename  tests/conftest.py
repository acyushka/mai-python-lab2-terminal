from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from services.history_service import HistoryService
from services.linux_console import LinuxConsoleService


@pytest.fixture
def fake_system(fs: FakeFilesystem) -> FakeFilesystem:
    fs.create_dir("/home/test/data1")
    fs.create_dir("/home/test/data2")
    fs.create_dir("/home/test/.data3")

    fs.create_file("/home/test/data1/test1.txt", contents="TEST 1")
    fs.create_file("/home/test/data1/test2.txt", contents="TEST 2")
    fs.create_file("/home/test/data1/empty.txt", contents="")
    fs.create_file("/home/test/testD.txt", contents="TEST D")
    fs.create_file("/home/test/.data3/.secret.txt", contents="SECRET")
    fs.create_file("/home/test/sym.txt", contents="GOOD SYMLINK")
    fs.create_symlink("/home/link.txt", "/home/test/sym.txt")
    fs.create_file("no_access.txt", contents="SECRET")
    fs.chmod("no_access.txt", 0o033)

    return fs

@pytest.fixture
def linux_console(fake_system: FakeFilesystem) -> LinuxConsoleService:
    service = LinuxConsoleService()
    service.current_path = Path("/home/test/")
    return service

@pytest.fixture
def history_service(fake_system: FakeFilesystem) -> HistoryService:
    return HistoryService()