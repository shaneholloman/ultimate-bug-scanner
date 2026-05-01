# Ruby UBS Samples

| File | Category |
|------|----------|
| `buggy/security_issues.rb` | eval, unsafe YAML |
| `buggy/resource_lifecycle.rb` | File/thread cleanup |
| `buggy/buggy_scripts.rb` | Shelling out, missing rescue |
| `buggy/performance.rb` | Thread leaks, backticks |
| `archive_extraction_buggy/zip_slip.rb` | RubyZip/TarReader/Minitar path traversal |
| `archive_extraction_clean/zip_slip_safe.rb` | `File.expand_path`/`Pathname` + `start_with?` containment checks |
| `path_traversal_buggy/request_paths.rb` | Rack/Rails params and upload names flowing to file read/write/serve/delete sinks |
| `path_traversal_clean/request_paths.rb` | `File.basename` upload names and `File.expand_path` + `start_with?` containment checks |
| Clean files | Managed threads, Open3 argv |

```bash
ubs --only=ruby --fail-on-warning test-suite/ruby/buggy
ubs --only=ruby test-suite/ruby/clean
```
