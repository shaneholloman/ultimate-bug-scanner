import os
import stat
from pathlib import Path

PUBLIC_FILE_MODE = 0o666
PUBLIC_DIR_MODE = 0o777


def chmod_world_writable(path):
    os.chmod(path, 0o777)


def chmod_named_mode(path):
    Path(path).chmod(PUBLIC_FILE_MODE)


def mkdir_world_writable(path):
    os.makedirs(path, mode=PUBLIC_DIR_MODE)


def pathlib_mkdir_world_writable(path):
    Path(path).mkdir(mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def os_open_world_writable(path):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o666)
    os.close(fd)


def permissive_umask():
    os.umask(0)
