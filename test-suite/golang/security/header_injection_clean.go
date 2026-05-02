package security

import (
	"mime"
	"net/http"
	"strings"
)

type cleanHeaderContext interface {
	Query(string) string
	Header(string, string)
}

func safeHeaderValue(raw string) string {
	return strings.NewReplacer("\r", "", "\n", "").Replace(raw)
}

func queryValueInSafeHeader(w http.ResponseWriter, r *http.Request) {
	displayName := safeHeaderValue(r.URL.Query().Get("name"))
	w.Header().Set("X-Display-Name", displayName)
}

func safeContentDisposition(w http.ResponseWriter, r *http.Request) {
	filename := r.FormValue("filename")
	disposition := mime.FormatMediaType("attachment", map[string]string{"filename": filename})
	w.Header().Set("Content-Disposition", disposition)
}

func guardedRequestHeader(w http.ResponseWriter, r *http.Request) {
	traceID := r.Header.Get("X-Trace-ID")
	if strings.ContainsAny(traceID, "\r\n") {
		http.Error(w, "invalid trace header", http.StatusBadRequest)
		return
	}
	w.Header().Add("X-Upstream-Trace", traceID)
}

func frameworkHeaderWithSafeHelper(c cleanHeaderContext) {
	c.Header("X-Return-Reason", safeHeaderValue(c.Query("reason")))
}
