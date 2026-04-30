import subprocess


COMMANDS = {
    "status": ["git", "status", "--short"],
    "version": ["git", "--version"],
}


def run_named_command(name):
    command = COMMANDS.get(name)
    if command is None:
        raise ValueError("unsupported command")
    return subprocess.run(command, check=True, shell=False, timeout=5)


def inspect_archive(archive_path):
    return subprocess.run(["tar", "-tf", str(archive_path)], check=True, timeout=5)


def static_executable_with_args(host):
    return subprocess.run(["ping", "-c", "1", str(host)], check=True, timeout=5)
