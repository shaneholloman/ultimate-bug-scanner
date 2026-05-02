package security

import (
	"net/http"
	"net/url"
	"strings"
)

func safeRedirectTarget(raw string) string {
	parsed, err := url.Parse(raw)
	if err != nil {
		return "/"
	}
	if parsed.IsAbs() {
		if parsed.Scheme == "https" && parsed.Hostname() == "app.example.com" {
			return parsed.String()
		}
		return "/"
	}
	if !strings.HasPrefix(parsed.Path, "/") || strings.HasPrefix(parsed.Path, "//") {
		return "/"
	}
	return parsed.String()
}

func redirectWithSafeHelper(w http.ResponseWriter, r *http.Request) {
	next := r.URL.Query().Get("next")
	http.Redirect(w, r, safeRedirectTarget(next), http.StatusFound)
}

func locationWithSafeHelper(w http.ResponseWriter, r *http.Request) {
	target := safeRedirectTarget(r.Header.Get("X-Return-To"))
	w.Header().Set("Location", target)
	w.WriteHeader(http.StatusFound)
}
