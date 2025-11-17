# Lightweight Taint Analysis TODO

## Research & Planning
- [x] Re-read Feature #4 section to enumerate sources, sinks, sanitizers.
- [x] Decide initial language scope (start with JS; list future targets for Python/Ruby/etc.).
- [x] Define metadata structures similar to async/hooks helpers (TAINT_RULE_IDS, summary, remediation, severity).

## Implementation (JavaScript module phase 1)
- [x] Implement taint helper `run_taint_analysis_checks` in `modules/ubs-js.sh`:
  - [x] Detect taint sources (req.body, req.query, window.location, event.target.value, localStorage, FormData).
  - [x] Track flows through assignments, template literals, function args/returns (lightweight heuristics).
  - [x] Match sinks (innerHTML, document.write, eval, Function, exec, db.query, child_process.exec, etc.).
  - [x] Respect simple sanitizers (DOMPurify.sanitize, escapeHtml, parameterized SQL).
  - [x] Emit findings with source→sink path descriptions.
- [x] Hook helper into JS module output (security category after eval/new Function checks).

## Fixtures & Testing
- [x] Create buggy JS fixtures showcasing XSS/SQL/command injection paths.
- [x] Create clean fixtures that sanitize input.
- [x] Add manifest cases for taint coverage (buggy should fail, clean should pass).
- [ ] Run targeted manifest cases (blocked: `ubs` currently reports `Files: 0` for single-file manifests; needs follow-up fix before this can pass).

## Documentation & Follow-up
- [x] Mention new taint capability in README/test-suite docs.
- [x] Outline plan for expanding to other languages (TODO in doc).

## Expansion Roadmap
- [ ] Python: port helper (asyncio.create_task, FastAPI request bodies, Django ORM sanitizers) and add fixtures/manifest coverage.
- [ ] Go: tag taint sources (http.Request.Form, json.Decoder) and sinks (template.Execute, exec.Command, `db.Exec` without args).
- [ ] Java/C++/Rust/Ruby: enumerate per-language sources/sinks + sanitizer heuristics; reuse helper structure for consistency.
