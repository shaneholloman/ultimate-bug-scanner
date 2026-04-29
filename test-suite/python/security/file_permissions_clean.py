import os
import stat
import tempfile
from pathlib import Path

PRIVATE_FILE_MODE = 0o600
PRIVATE_DIR_MODE = 0o700


def chmod_private_file(path):
    os.chmod(path, PRIVATE_FILE_MODE)


def chmod_group_readable_file(path):
    Path(path).chmod(0o640)


def mkdir_private_directory(path):
    os.makedirs(path, mode=PRIVATE_DIR_MODE)


def pathlib_mkdir_private_directory(path):
    Path(path).mkdir(mode=stat.S_IRWXU)


def os_open_private_file(path):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o600)
    os.close(fd)


def restrictive_umask():
    os.umask(0o077)


def secure_tempfile():
    with tempfile.NamedTemporaryFile() as handle:
        handle.write(b"secret")
