package security

import (
	"io"
	"net/http"
)

const maxBodyBytes int64 = 1 << 20

func importPayload(w http.ResponseWriter, r *http.Request) ([]byte, error) {
	r.Body = http.MaxBytesReader(w, r.Body, maxBodyBytes)
	return io.ReadAll(r.Body)
}

func readLimitedUpload(r *http.Request) ([]byte, error) {
	limited := io.LimitReader(r.Body, maxBodyBytes)
	return io.ReadAll(limited)
}
