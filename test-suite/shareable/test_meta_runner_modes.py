#!/usr/bin/env python3
"""Regression tests for UBS meta-runner modes that do not scan a checkout."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UBS_BIN = REPO_ROOT / "ubs"


def run_ubs(args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    merged_env.update(env)
    return subprocess.run(
        [str(UBS_BIN), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=merged_env,
        check=False,
    )


def assert_not_size_guarded(result: subprocess.CompletedProcess[str]) -> None:
    output = result.stdout + result.stderr
    assert "Directory too large" not in output, output
    assert "Refusing to scan" not in output, output


def main() -> None:
    tmpdir = Path(tempfile.mkdtemp(prefix="ubs-meta-runner-"))
    try:
        tight_limit_env = {
            "NO_COLOR": "1",
            "UBS_MAX_DIR_SIZE_MB": "1",
            "UBS_SKIP_SIZE_CHECK": "0",
            "UBS_ENABLE_AUTO_UPDATE": "0",
        }

        doctor = run_ubs(["doctor", f"--module-dir={tmpdir / 'modules'}"], tight_limit_env)
        assert doctor.returncode == 0, doctor.stdout + doctor.stderr
        assert "UBS Doctor" in doctor.stdout, doctor.stdout + doctor.stderr
        assert_not_size_guarded(doctor)

        update = run_ubs(["--update", "--quiet"], tight_limit_env)
        assert update.returncode == 0, update.stdout + update.stderr
        assert_not_size_guarded(update)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
