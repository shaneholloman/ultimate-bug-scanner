# Python UBS Samples

| File | Category | What UBS should flag |
|------|----------|----------------------|
| `buggy/buggy_async_security.py` | Async/await pitfalls + insecure requests | unguarded awaits, missing try/except, `verify=False` |
| `buggy/resource_lifecycle.py` | File/task cleanup | missing `close()`/`cancel()` |
| `buggy/security_injection.py` | Code & command injection, yaml.load, eval | eval/exec, yaml.load without Loader, shell=True |
| `security/archive_extraction_buggy.py` | Archive extraction security | tarfile/zipfile `extractall()` without member path validation |
| `security/open_redirect_buggy.py` | Web redirect security | request-derived Flask/Django/Starlette redirect targets without allow-list validation |
| `security/ssrf_buggy.py` | Outbound HTTP security | request-derived URLs reaching requests/httpx/aiohttp/urllib clients without host allow-list validation |
| `security/path_traversal_buggy.py` | File download security | request-derived paths reaching `open`, `send_file`, `FileResponse`, or `Path.read_*` without containment validation |
| `security/jwt_verification_buggy.py` | JWT verification security | `jwt.decode` calls that disable signature/claim checks or allow `algorithms=["none"]` |
| `security/cors_misconfig_buggy.py` | CORS configuration security | credentialed Flask-CORS, Starlette/FastAPI, or Django CORS configs that allow wildcard origins |
| `security/cookie_security_buggy.py` | Cookie/session security | Django/Flask cookie settings or response cookies that disable Secure/HttpOnly or use SameSite=None without Secure |
| `security/debug_host_config_buggy.py` | Debug/host configuration security | production debug flags, debugger-enabled app runs, and wildcard host allow-lists |
| `security/xml_parser_buggy.py` | XML parser security | request/upload XML parsed by stdlib/lxml parsers or lxml parsers with DTD/entity-expansion flags |
| `buggy/mutable_defaults.py` | Function scope issues | mutable defaults, swallowed exceptions, weak hash |
| `clean/*.py` mirrors | Defensive patterns | safe YAML, parameterized SQL, integer cents |

Run:

```bash
ubs --only=python --fail-on-warning test-suite/python/buggy
ubs --only=python test-suite/python/clean
```
