from flask import request
import os
import subprocess as sp
from subprocess import check_output as command_output


def shell_command_from_query():
    archive = request.args["archive"]
    command = f"tar -tf {archive}"
    return sp.run(command, shell=True, check=False)


def shell_c_from_query():
    branch = request.args.get("branch", "main")
    return sp.check_call(["bash", "-lc", f"git show {branch}"], cwd="/srv/repo")


def request_selected_executable():
    tool = request.args.get("tool", "git")
    return sp.call([tool, "--version"])


def os_system_from_stdin():
    host = input("host: ")
    return os.system("ping -c 1 " + host)


def aliased_subprocess_shell():
    command = request.form["command"]
    return command_output(command, shell=True)
