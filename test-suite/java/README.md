# Java UBS Samples

| File | Focus |
|------|-------|
| `buggy/BuggyService.java` | Blocking I/O, TLS issues |
| `buggy/BuggyConcurrency.java` | ExecutorService leaks, missing shutdown |
| `buggy/ResourceLifecycle.java` | Streams not closed |
| `buggy/BuggySecurity.java` | SQL/command injection |
| `security/path_traversal_buggy.java` | request parameters and upload filenames reaching file read/write/delete sinks without containment checks |
| `security/path_traversal_clean.java` | canonical root containment and basename extraction before file sinks |
| `security/SsrfBuggy.java` | request parameters, headers, and servlet host accessors reaching outbound HTTP clients |
| `security/SsrfClean.java` | safe outbound URL helpers with scheme and host allow-list validation |
| `security/ArchiveExtractionBuggy.java` | Archive extraction security |
| `security/ArchiveExtractionClean.java` | normalize + startsWith destination checks |
| Clean files | try-with-resources, prepared statements, ProcessBuilder argv |

```bash
ubs --only=java --fail-on-warning test-suite/java/buggy
ubs --only=java test-suite/java/clean
```
