package security

import (
	"archive/tar"
	"archive/zip"
	"errors"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func safeDestination(destination, name string) (string, error) {
	if filepath.IsAbs(name) {
		return "", errors.New("archive member escapes destination")
	}

	target := filepath.Join(destination, name)
	relative, err := filepath.Rel(destination, target)
	if err != nil {
		return "", err
	}
	if relative == "." || relative == ".." || strings.HasPrefix(relative, ".."+string(os.PathSeparator)) {
		return "", errors.New("archive member escapes destination")
	}
	return target, nil
}

func UnzipSafely(archivePath, destination string) error {
	reader, err := zip.OpenReader(archivePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	for _, file := range reader.File {
		target, err := safeDestination(destination, file.Name)
		if err != nil {
			return err
		}
		if file.FileInfo().IsDir() {
			if err := os.MkdirAll(target, 0o755); err != nil {
				return err
			}
			continue
		}

		source, err := file.Open()
		if err != nil {
			return err
		}
		output, err := os.Create(target)
		if err != nil {
			source.Close()
			return err
		}
		if _, err := io.Copy(output, source); err != nil {
			source.Close()
			output.Close()
			return err
		}
		source.Close()
		output.Close()
	}
	return nil
}

func UntarSafely(archivePath, destination string) error {
	archive, err := os.Open(archivePath)
	if err != nil {
		return err
	}
	defer archive.Close()

	reader := tar.NewReader(archive)
	for {
		header, err := reader.Next()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		target, err := safeDestination(destination, header.Name)
		if err != nil {
			return err
		}
		if header.FileInfo().IsDir() {
			if err := os.MkdirAll(target, 0o755); err != nil {
				return err
			}
			continue
		}

		output, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, os.FileMode(header.Mode))
		if err != nil {
			return err
		}
		if _, err := io.Copy(output, reader); err != nil {
			output.Close()
			return err
		}
		output.Close()
	}
}
