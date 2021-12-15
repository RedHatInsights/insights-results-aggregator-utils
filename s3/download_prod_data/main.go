package main

import (
	"os"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

const (
	maxKeys         = 1000
	downloadsFolder = "downloads"
)

func init() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

}

func main() {
	config := getConfig()
	log.Debug().
		Interface("config", config).
		Interface("s3 config", config.s3config).
		Msg("Configuration")

	s3client, err := getClient(config.s3config)
	checkError(err)

	clusters, err := getClusters(s3client, config.s3config, config.NClusters)
	checkError(err)

	f, w, err := initCSV(config.CSVpath)
	checkError(err)
	defer closeCSV(f, w)

	log.Debug().Strs("selected clusters", clusters).Msg("Clusters")

	for i := range clusters {
		tarBalls, err := getNTarBalls(s3client, config.s3config, clusters[i], config.NTarballs)
		checkError(err)
		for j := range tarBalls {
			err = downloadTarball(s3client, config.s3config, tarBalls[j])
			checkError(err)
			err = writeRow(w, clusters[i], tarBalls[j])
			checkError(err)
		}
	}
	checkError(err)
}

func checkError(err error) {
	if err != nil {
		os.Exit(1)
	}
}
