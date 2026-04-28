package security

import (
	"archive/tar"
	"archive/zip"
	"io"
	"os"
	"path/filepath"
)

func UnzipUnsafe(archivePath, destination string) error {
	reader, err := zip.OpenReader(archivePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	for _, file := range reader.File {
		target := filepath.Join(destination, file.Name)
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

func UntarUnsafe(archivePath, destination string) error {
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

		target := filepath.Join(destination, header.Name)
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
