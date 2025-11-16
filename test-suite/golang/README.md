# Go UBS Samples

- Buggy fixtures: `buggy_http.go`, `buggy_concurrency.go` trigger TLS, exec, and WaitGroup alarms.
- Clean fixtures ensure contexts are cancelled and http.Clients have timeouts.
- Run `ubs test-suite/golang/buggy` vs `ubs test-suite/golang/clean`.
