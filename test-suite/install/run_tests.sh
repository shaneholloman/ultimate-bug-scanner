#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INSTALLER="$ROOT_DIR/install.sh"

tests_failed=0
tmpdirs=()

cleanup() {
  for dir in "${tmpdirs[@]:-}"; do
    rm -rf "$dir"
  done
}
trap cleanup EXIT

run_installer() {
  local home_dir="$1"
  local log_file="$2"
  shift 2

  local bin_dir="$home_dir/.local/bin"
  mkdir -p "$bin_dir"

  if ! HOME="$home_dir" PATH="$bin_dir:$PATH" SHELL=/bin/bash \
      "$INSTALLER" \
        --non-interactive \
        --skip-ast-grep \
        --skip-ripgrep \
        --skip-jq \
        --skip-hooks \
        --skip-version-check \
        --no-path-modify \
        --install-dir "$bin_dir" \
        "$@" >"$log_file" 2>&1; then
    echo "[FAIL] Installer exited with status $? (log: $log_file)"
    tail -n 80 "$log_file"
    tests_failed=1
    return 1
  fi

  if ! grep -q "POST-INSTALL VERIFICATION" "$log_file"; then
    echo "[FAIL] Verification block missing (log: $log_file)"
    tests_failed=1
    return 1
  fi

  if [ ! -x "$bin_dir/ubs" ]; then
    echo "[FAIL] ubs binary not installed at $bin_dir/ubs"
    tests_failed=1
    return 1
  fi

  return 0
}

test_basic_smoke() {
  echo "[TEST] basic_smoke"
  local ctx
  ctx="$(mktemp -d)"
  tmpdirs+=("$ctx")
  local home="$ctx/home"
  local log="$ctx/install.log"

  if run_installer "$home" "$log"; then
    if grep -q "typos not found" "$log"; then
      echo "[PASS] typos warning emitted"
    else
      echo "[FAIL] expected typos warning missing (log: $log)"
      tests_failed=1
      return
    fi
    echo "[PASS] basic_smoke"
  fi
}

test_no_alias_written_when_no_path_modify() {
  echo "[TEST] no_alias_with_no_path_modify"
  local ctx
  ctx="$(mktemp -d)"
  tmpdirs+=("$ctx")
  local home="$ctx/home"
  mkdir -p "$home"
  local rc_file="$home/.bashrc"
  echo "# Sentinel file" >"$rc_file"
  cp "$rc_file" "$rc_file.before"
  local log="$ctx/install.log"

  if run_installer "$home" "$log"; then
    if cmp -s "$rc_file" "$rc_file.before"; then
      echo "[PASS] no_alias_with_no_path_modify"
    else
      echo "[FAIL] rc file modified despite --no-path-modify"
      diff -u "$rc_file.before" "$rc_file" || true
      tests_failed=1
    fi
  fi
}

test_skip_typos_flag() {
  echo "[TEST] skip_typos_flag"
  local ctx
  ctx="$(mktemp -d)"
  tmpdirs+=("$ctx")
  local home="$ctx/home"
  local log="$ctx/install.log"

  if run_installer "$home" "$log" --skip-typos; then
    if grep -q "typos not found" "$log"; then
      echo "[FAIL] typos warning appeared despite --skip-typos"
      tests_failed=1
    else
      echo "[PASS] skip_typos_flag"
    fi
  fi
}

test_basic_smoke
test_no_alias_written_when_no_path_modify
test_skip_typos_flag

if [ "$tests_failed" -ne 0 ]; then
  echo ""
  echo "[RESULT] Installer tests failed."
  exit 1
fi

echo ""
echo "[RESULT] All installer tests passed."
