#!/usr/bin/env python3
"""Regression tests for the C# helper analyzers."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TYPE_HELPER = REPO_ROOT / "modules" / "helpers" / "type_narrowing_csharp.py"
RESOURCE_HELPER = REPO_ROOT / "modules" / "helpers" / "resource_lifecycle_csharp.py"


def run_helper(helper: Path, sources: dict[str, str]) -> list[str]:
    temp_dir = Path(tempfile.mkdtemp(prefix="ubs-csharp-helper-"))
    try:
        for rel, code in sources.items():
            path = temp_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(code), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(helper), str(temp_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        return [line for line in result.stdout.splitlines() if line.strip()]
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


class CSharpHelperTests(unittest.TestCase):
    def test_type_narrowing_helper_reports_guard_fallthrough(self) -> None:
        lines = run_helper(
            TYPE_HELPER,
            {
                "buggy.cs": """
                using System;
                using System.Collections.Generic;

                class Demo {
                    int Run(string rawInput, Dictionary<string, string> cache) {
                        if (rawInput == null) {
                            Console.WriteLine("missing");
                        }
                        if (!cache.TryGetValue("token", out var token)) {
                            Console.WriteLine("missing token");
                        }
                        return rawInput.Trim().Length + token.Length;
                    }
                }
                """,
            },
        )
        self.assertTrue(any("rawInput dereferenced after non-exiting null/empty guard" in line for line in lines))
        self.assertTrue(any("token used after non-exiting TryGetValue guard" in line for line in lines))

    def test_type_narrowing_helper_stays_quiet_for_clean_guards(self) -> None:
        lines = run_helper(
            TYPE_HELPER,
            {
                "clean.cs": """
                using System.Collections.Generic;

                class Demo {
                    int? Run(string rawInput, Dictionary<string, string> cache) {
                        if (string.IsNullOrWhiteSpace(rawInput)) {
                            return null;
                        }
                        if (!cache.TryGetValue("token", out var token)) {
                            return null;
                        }
                        return rawInput.Trim().Length + token.Length;
                    }
                }
                """,
            },
        )
        self.assertEqual(lines, [])

    def test_resource_helper_reports_disposable_leaks(self) -> None:
        lines = run_helper(
            RESOURCE_HELPER,
            {
                "leaky.cs": """
                using System.IO;
                using System.Net.Http;
                using System.Threading;

                class Demo {
                    void Leak() {
                        var cts = new CancellationTokenSource();
                        var reader = new StreamReader(new MemoryStream());
                        var request = new HttpRequestMessage(HttpMethod.Get, "https://example.com");
                    }
                }
                """,
            },
        )
        self.assertTrue(any("CancellationTokenSource acquired without Dispose" in line for line in lines))
        self.assertTrue(any("Stream-like handle acquired without using/Dispose/Close" in line for line in lines))
        self.assertTrue(any("HttpRequestMessage created without Dispose" in line for line in lines))

    def test_resource_helper_ignores_using_var_cleanup(self) -> None:
        lines = run_helper(
            RESOURCE_HELPER,
            {
                "clean.cs": """
                using System.IO;
                using System.Net.Http;
                using System.Threading;

                class Demo {
                    void Tidy() {
                        using var cts = new CancellationTokenSource();
                        using var reader = new StreamReader(new MemoryStream());
                        using var request = new HttpRequestMessage(HttpMethod.Get, "https://example.com");
                    }
                }
                """,
            },
        )
        self.assertEqual(lines, [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
