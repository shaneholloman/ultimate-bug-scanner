# Rust UBS Samples

| File | Category |
|------|----------|
| `buggy/buggy_unwrap.rs` | Panic-prone unwrap chains |
| `buggy/async_block.rs` | Spawned tasks never awaited |
| `buggy/blocking_async.rs` | Blocking sleep/fs/thread operations inside async functions |
| `buggy/resource_lifecycle.rs` | Missing JoinHandle cleanup |
| `buggy/security_injection.rs` | Command injection + exposed secrets |
| `buggy/archive_extraction.rs` | Archive member paths joined into extraction destinations |
| `buggy/temp_file_race.rs` | Predictable temp-file writes in shared temp directories |
| `buggy/math_precision.rs` | Float equality for money |
| Clean files (`clean/*.rs`) | `Result` handling, JoinHandle waiting, integer cents, safe temp-file creation |

```bash
ubs --only=rust --fail-on-warning test-suite/rust/buggy
ubs --only=rust test-suite/rust/clean
```
