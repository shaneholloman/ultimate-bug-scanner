import subprocess as sp
from subprocess import check_output, run as run_process

import subprocess


def run_git_status() -> subprocess.CompletedProcess:
    return subprocess.run(["git", "status", "--short"], check=True, timeout=5)


def run_alias() -> subprocess.CompletedProcess:
    return sp.run(["git", "--version"], check=True, timeout=5)


def run_direct_import() -> subprocess.CompletedProcess:
    return run_process(["python3", "--version"], check=True, timeout=5)


def capture_output() -> bytes:
    return check_output(["git", "rev-parse", "HEAD"], timeout=5)


def dynamic_timeout(deadline_seconds: float) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "status"], check=True, timeout=deadline_seconds)
