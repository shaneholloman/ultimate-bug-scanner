import subprocess as sp
from subprocess import check_output, run as run_process

import subprocess


def run_git_status() -> subprocess.CompletedProcess:
    return subprocess.run(["git", "status", "--short"], check=True)


def run_alias() -> subprocess.CompletedProcess:
    return sp.run(["git", "--version"], check=True)


def run_direct_import() -> subprocess.CompletedProcess:
    return run_process(["python3", "--version"], check=True)


def capture_output() -> bytes:
    return check_output(["git", "rev-parse", "HEAD"])


def legacy_shell_output() -> str:
    return subprocess.getoutput("git status --short")


def explicit_unbounded_timeout() -> subprocess.CompletedProcess:
    return subprocess.run(["git", "status"], check=True, timeout=None)
