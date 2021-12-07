package main

import (
	"os"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

const (
	maxKeys         = 1000
	nTarballs       = 1
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
	if err != nil {
		return
	}
	clusters, err := getClusters(s3client, config.s3config, config.NClusters)
	if err != nil {
		return
	}

	log.Debug().Strs("selected clusters", clusters).Msg("Clusters")

	for i := range clusters {
		err = downloadNTarballs(s3client, config.s3config, clusters[i], nTarballs)
	}
	if err != nil {
		return
	}
}
