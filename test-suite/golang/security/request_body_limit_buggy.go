package security

import (
	"io"
	"io/ioutil"
	"net/http"
)

func importPayload(r *http.Request) ([]byte, error) {
	return io.ReadAll(r.Body)
}

func legacyUpload(req *http.Request) ([]byte, error) {
	body, err := ioutil.ReadAll(req.Body)
	if err != nil {
		return nil, err
	}
	return body, nil
}
