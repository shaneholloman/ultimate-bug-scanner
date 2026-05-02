package security

import "net/http"

type headerContext interface {
	Query(string) string
	Header(string, string)
	Set(string, string)
}

func queryValueInHeader(w http.ResponseWriter, r *http.Request) {
	displayName := r.URL.Query().Get("name")
	w.Header().Set("X-Display-Name", displayName)
}

func formValueInContentDisposition(w http.ResponseWriter, r *http.Request) {
	filename := r.FormValue("filename")
	w.Header().Set("Content-Disposition", "attachment; filename="+filename)
}

func requestHeaderReflected(w http.ResponseWriter, r *http.Request) {
	traceID := r.Header.Get("X-Trace-ID")
	w.Header().Add("X-Upstream-Trace", traceID)
}

func frameworkHeaderFromQuery(c headerContext) {
	c.Header("X-Return-Reason", c.Query("reason"))
	c.Set("X-Mode", c.Query("mode"))
}
