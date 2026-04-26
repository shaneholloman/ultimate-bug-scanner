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


def assert_no_function_not_found(result: subprocess.CompletedProcess[str]) -> None:
    """Issue #44 regression guard: bash exits 127 with 'command not found'
    when a function is referenced before its definition. The
    --suggest-ignore feature shipped broken because suggest_ignore_candidates
    was defined ~470 lines below its call site. Catch any future
    function-order regression before it ships again."""
    output = result.stdout + result.stderr
    assert "command not found" not in output, output
    assert "(exit 127)" not in output, output


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

        # Issue #44: --suggest-ignore exited 127 because
        # suggest_ignore_candidates was called before its definition.
        # Build a tiny project tree with a recognizable language so
        # the meta-runner reaches the suggestion path (an "empty"
        # tree with no recognized files exits early before the
        # function would be called).
        scan_dir = tmpdir / "scan_target"
        (scan_dir / "src").mkdir(parents=True)
        (scan_dir / "src" / "main.rs").write_text("fn main() {}\n")
        (scan_dir / "Cargo.toml").write_text(
            '[package]\nname = "t"\nversion = "0.0.0"\nedition = "2021"\n'
        )
        suggest = subprocess.run(
            [str(UBS_BIN), "--suggest-ignore", str(scan_dir)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "NO_COLOR": "1", "UBS_ENABLE_AUTO_UPDATE": "0"},
            check=False,
        )
        # Function order is the failure mode being guarded against;
        # a non-zero exit from a downstream module is allowed (we don't
        # control what the rust scanner finds in `fn main() {}`), but
        # bash itself must never report "command not found".
        assert_no_function_not_found(suggest)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
