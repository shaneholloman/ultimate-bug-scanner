package security

import (
	"errors"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const cleanUploadRoot = "/srv/app/uploads"

func safeUploadPath(raw string) (string, error) {
	root := filepath.Clean(cleanUploadRoot)
	target := filepath.Join(root, raw)
	rel, err := filepath.Rel(root, target)
	if err != nil {
		return "", err
	}
	if filepath.IsAbs(rel) || rel == ".." || strings.HasPrefix(rel, "../") {
		return "", errors.New("path escapes upload root")
	}
	return target, nil
}

func downloadCleanFile(w http.ResponseWriter, r *http.Request) error {
	target, err := safeUploadPath(r.URL.Query().Get("file"))
	if err != nil {
		return err
	}
	http.ServeFile(w, r, target)
	return nil
}

func readCleanRouteFile(r *http.Request) ([]byte, error) {
	target, err := safeUploadPath(r.PathValue("name"))
	if err != nil {
		return nil, err
	}
	return os.ReadFile(target)
}

func saveCleanUploadedAvatar(r *http.Request) error {
	_, header, err := r.FormFile("avatar")
	if err != nil {
		return err
	}

	name := filepath.Base(header.Filename)
	target := filepath.Join(cleanUploadRoot, name)
	return os.WriteFile(target, []byte("avatar"), 0o600)
}

func downloadCleanHeaderFile(w http.ResponseWriter, r *http.Request) error {
	target, err := safeUploadPath(r.Header.Get("X-File-Path"))
	if err != nil {
		return err
	}
	http.ServeFile(w, r, target)
	return nil
}

func readCleanHeaderFile(req *http.Request) ([]byte, error) {
	target, err := safeUploadPath(req.Header.Get("X-Report-Path"))
	if err != nil {
		return nil, err
	}
	return os.ReadFile(target)
}
