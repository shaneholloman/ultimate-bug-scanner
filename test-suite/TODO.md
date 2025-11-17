# Test Suite TODO

- [x] Define manifest schema for UBS cases (paths, args, expectations, skip reasons).
- [x] Implement manifest-driven runner (`test-suite/run_manifest.py`) that executes UBS, parses JSON, and enforces expectations.
- [x] Seed manifest with JS coverage (core buggy/clean, framework scenarios, realistic cases) using `--only=js` where appropriate.
- [x] Connect the new runner to developer workflow (document usage in `test-suite/README.md`, wire optional helper script).
- [x] Capture run artifacts per case (stdout/stderr, parsed summary) to simplify debugging failed scanners.
- [ ] Add substring/rule-id requirement checks so we can prove specific categories fire.
- [x] Extend manifest to Python fixtures once parser stabilizes; include both `test-suite/python/buggy` and `python/clean` directories.
- [ ] Extend manifest to Go, Rust, C++, Java, Ruby fixtures in `test-suite/<lang>/`.
- [ ] Investigate why `modules/ubs-js.sh` sometimes reports `Files scanned: 0` even when files exist.
- [ ] Add threshold coverage for edge-case fixtures (unicode, floating-point, timezone).
- [ ] Wire manifest runner into CI once other modules catch up.

## Resource lifecycle fixtures (ultimate_bug_scanner-6ig)
- [ ] Investigate `modules/ubs-python.sh` single-file runs (resource_lifecycle) reporting zero files/warnings.
- [ ] Do the same for Go and Java fixtures (confirm detection logic).
- [ ] Restore warnings so `--fail-on-warning` triggers and manifest passes.

## Non-JS manifest expansion & docs (ultimate_bug_scanner-ny5)
- [ ] Update `test-suite/README.md` with a multi-language overview, manifest instructions, and tables listing every language’s buggy/clean directories.
  - [ ] Add a quick-start matrix covering JS, Python, Go, C++, Rust, Java, and Ruby fixtures plus their expected categories.
  - [ ] Document how `run_manifest.py` and `run_all.sh` interact so new contributors know which tool to run.
- [ ] Flesh out per-language READMEs with file-level descriptions modeled after the JS documentation.
- [ ] Expand fixture coverage in each non-JS directory to cover multiple categories (security, resource lifecycle, async, math/precision where applicable) with clean counterparts.
  - [ ] Python: add security + precision fixtures (buggy & clean) and describe them in README.
  - [ ] Go: add security/performance fixtures and README notes.
  - [ ] C++: add unsafe string/math fixtures and README notes.
  - [ ] Rust: add security/math fixtures and README notes.
  - [ ] Java: add security fixture pair and README notes.
  - [ ] Ruby: add performance/concurrency fixture pair and README notes.
- [ ] Add manifest coverage for every language’s `buggy` and `clean` directories (cpp/rust/java/ruby still missing) with severity thresholds + substring checks for signature sections.
- [ ] Add manifest cases for JS edge-case directories (unicode/timezone/floating-point) with warning thresholds so regressions surface.
- [ ] Extend manifest expectations to include category substrings for the new cases so we prove specific analyzers fire.
- [ ] Update `run_all.sh` to delegate to `run_manifest.py` (or drive manifest cases directly) instead of running bare directory scans.
- [ ] Run the refreshed manifest end-to-end, capture artifacts, and record the date/result in `notes/` for future baselines.

_Last updated: 2025-11-17 00:10 UTC_
