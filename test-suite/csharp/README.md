# C# Fixtures

- `buggy/` contains intentionally unsafe patterns for `ubs-csharp.sh`.
- `clean/` provides counterexamples that should stay free of critical/warning findings.
- `tests/test_helper_scanners.py` covers the helper-backed type narrowing and resource lifecycle analyzers directly.
- Manifest cases run with `--no-dotnet` so scanner regressions stay stable even when the .NET SDK is absent.
