# Python UBS Samples

| File | Category | What UBS should flag |
|------|----------|----------------------|
| `buggy/buggy_async_security.py` | Async/await pitfalls + insecure requests | unguarded awaits, missing try/except, `verify=False` |
| `buggy/resource_lifecycle.py` | File/task cleanup | missing `close()`/`cancel()` |
| `buggy/security_injection.py` | Code & command injection, yaml.load, eval | eval/exec, yaml.load without Loader, shell=True |
| `security/command_injection_buggy.py` | Command execution security | request/stdin data reaching `shell=True`, shell `-c`, `os.system`, aliased subprocess calls, or executable selection |
| `security/sql_injection_buggy.py` | SQL injection security | f-string, `%`, `.format()`, and concatenated SQL reaching execute/raw/extra/read_sql sinks |
| `security/archive_extraction_buggy.py` | Archive extraction security | tarfile/zipfile `extractall()` without member path validation |
| `security/open_redirect_buggy.py` | Web redirect security | request-derived Flask/Django/Starlette redirect targets without allow-list validation |
| `security/ssrf_buggy.py` | Outbound HTTP security | request-derived URLs reaching requests/httpx/aiohttp/urllib clients without host allow-list validation |
| `security/http_timeout_buggy.py` | Outbound HTTP reliability | requests/httpx/aiohttp/urllib/urllib3 calls or clients without explicit bounded timeouts |
| `security/path_traversal_buggy.py` | File download/upload security | request-derived paths reaching `open`, `send_file`, `FileResponse`, `Path.read_*`, or uploaded-file `save()` without containment validation |
| `security/jwt_verification_buggy.py` | JWT verification security | `jwt.decode` calls that disable signature/claim checks or allow `algorithms=["none"]` |
| `security/cors_misconfig_buggy.py` | CORS configuration security | credentialed Flask-CORS, Starlette/FastAPI, or Django CORS configs that allow wildcard origins |
| `security/cookie_security_buggy.py` | Cookie/session security | Django/Flask cookie settings or response cookies that disable Secure/HttpOnly or use SameSite=None without Secure |
| `security/csrf_disable_buggy.py` | CSRF protection security | Django `csrf_exempt`, Flask-WTF exemptions, and settings that disable CSRF checks |
| `security/template_autoescape_buggy.py` | Template/XSS security | Jinja2/Flask template environments and options that disable autoescape |
| `security/mass_assignment_buggy.py` | Mass-assignment security | request dictionaries passed into model constructors, ORM creates/updates, object updates, or `setattr` loops |
| `security/unsafe_deserialization_buggy.py` | Deserialization security | marshal/dill/cloudpickle/joblib/jsonpickle/shelve/pandas/yaml unsafe loaders, NumPy pickle arrays, and unsafe torch checkpoints |
| `security/password_hashing_buggy.py` | Password hashing security | plaintext, MD5, SHA1, unsalted, or legacy Django/Werkzeug/Passlib password hashers |
| `security/debug_host_config_buggy.py` | Debug/host configuration security | production debug flags, debugger-enabled app runs, and wildcard host allow-lists |
| `security/xml_parser_buggy.py` | XML parser security | request/upload XML parsed by stdlib/lxml parsers or lxml parsers with DTD/entity-expansion flags |
| `security/random_security_buggy.py` | Security randomness | tokens, sessions, OTPs, salts, and keys generated with the non-cryptographic `random` module |
| `security/tls_verification_buggy.py` | TLS verification security | `httpx`, `aiohttp`, `urllib3`, and `ssl` configurations that disable certificate or hostname checks |
| `buggy/mutable_defaults.py` | Function scope issues | mutable defaults, swallowed exceptions, weak hash |
| `clean/*.py` mirrors | Defensive patterns | safe YAML, parameterized SQL, integer cents |

Run:

```bash
ubs --only=python --fail-on-warning test-suite/python/buggy
ubs --only=python test-suite/python/clean
```
