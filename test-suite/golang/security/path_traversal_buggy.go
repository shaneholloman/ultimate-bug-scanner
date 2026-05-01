package security

import (
	"net/http"
	"os"
	"path/filepath"
)

const publicUploadRoot = "/srv/app/uploads"

func downloadQueryFile(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("file")
	http.ServeFile(w, r, filepath.Join(publicUploadRoot, name))
}

func readRouteFile(r *http.Request) ([]byte, error) {
	name := r.PathValue("name")
	return os.ReadFile(filepath.Join(publicUploadRoot, name))
}

func saveUploadedAvatar(r *http.Request) error {
	_, header, err := r.FormFile("avatar")
	if err != nil {
		return err
	}

	target := filepath.Join(publicUploadRoot, header.Filename)
	return os.WriteFile(target, []byte("avatar"), 0o600)
}

func removeRequestedFile(r *http.Request) error {
	target := filepath.Join(publicUploadRoot, r.FormValue("delete"))
	return os.Remove(target)
}
