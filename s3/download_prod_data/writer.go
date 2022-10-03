package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"

	"github.com/rs/zerolog/log"
)

const filePermissions fs.FileMode = 0o0700

func writeToPath(path string, content []byte) error {
	filePath := fmt.Sprintf("%s/%s", downloadsFolder, path)
	filePathFolder, _ := filepath.Split(filePath)
	if _, err := os.Stat(filePathFolder); os.IsNotExist(err) {
		log.Debug().Str("folder", filePathFolder).Msg("Creating folder")
		err := os.MkdirAll(filePathFolder, filePermissions)
		if err != nil {
			log.Error().Err(err).Str("folder", filePathFolder).Msg("Error creating the folder")
			return err
		}
	}

	log.Debug().Str("archive_path", path).Msg("Writing tarball")
	if err := os.WriteFile(filePath, content, filePermissions); err != nil {
		log.Error().Err(err).Str("archive_path", path).Msg("Error writing tarball")
		return err
	}
	return nil
}
