package main

import (
	"encoding/csv"
	"errors"
	"os"

	"github.com/rs/zerolog/log"
)

func initCSV(csvPath string) (*os.File, *csv.Writer, error) {
	if csvPath == "" {
		err := errors.New("no csv path provided")
		log.Error().Err(err).Msg("error initializing the csv writer")
		return nil, nil, err
	}
	f, err := os.Create(csvPath)

	if err != nil {
		log.Error().Err(err).Str("file", csvPath).Msg("cannot open file")
		return nil, nil, err
	}

	w := csv.NewWriter(f)
	err = writeRow(w, "cluster", "tarball")
	if err != nil {
		log.Error().Err(err).Str("file", csvPath).Msg("error writing header")
		return nil, nil, err
	}
	return f, w, err
}

func closeCSV(f *os.File, w *csv.Writer) {
	log.Debug().Msg("Closing CSV")
	w.Flush()
	if err := w.Error(); err != nil {
		log.Error().Err(err).Msg("error flushing writer")
	}

	if err := f.Close(); err != nil {
		log.Error().Err(err).Msg("error closing file")
	}
}

func writeRow(w *csv.Writer, cluster, tarBall string) error {
	log.Debug().Str("cluster", cluster).
		Str("tarBall", tarBall).Msg("writing row")
	err := w.Write([]string{cluster, tarBall})
	if err != nil {
		log.Error().
			Err(err).
			Str("cluster", cluster).
			Str("tarBall", tarBall).
			Msg("cannot open file")
	}
	return err
}
