# JavaScript/TypeScript UBS Mini Suite

- `buggy/security.js` contains eval, innerHTML, and missing error handling.
- `clean/security.js` shows the safe equivalents.
- `buggy/resource-lifecycle.js` and `clean/resource-lifecycle.js` cover browser resource cleanup, including Blob/Object URL revocation.
- `security/dangerously-set-html-*.tsx` covers TypeScript/React XSS risk from unsanitized `dangerouslySetInnerHTML`.
- `security/target-blank-*.tsx` covers TypeScript/React reverse-tabnabbing protection for JSX `target="_blank"` links.
- `security/window-open-*.ts` covers TypeScript reverse-tabnabbing protection for `window.open(..., "_blank")`.
- `resource_lifecycle/object-url-*.ts` covers TypeScript Blob/Object URL cleanup regression samples.
- These smaller samples complement the full `test-suite/buggy` / `clean` collections and are used by the automated runner.
