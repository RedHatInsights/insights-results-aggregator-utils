package main

import (
	s3util "github.com/RedHatInsights/insights-operator-utils/s3"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/rs/zerolog/log"
)

func getClient(s3config S3config) (*s3.S3, error) {
	sess, err := session.NewSession(&aws.Config{
		Credentials: credentials.NewStaticCredentials(s3config.AccessKey, s3config.SecretKey, ""),
		Endpoint:    aws.String(s3config.Endpoint),
		Region:      aws.String(s3config.Region),
		DisableSSL:  aws.Bool(s3config.DisableSSL),
	})
	if err != nil {
		log.Error().Err(err).Msg("error instantiating client")
		return nil, err
	}
	s3Client := s3.New(sess)
	_, err = s3Client.HeadBucket(&s3.HeadBucketInput{
		Bucket: &s3config.Bucket,
	})
	if err != nil {
		log.Error().Err(err).Msg("cannot connect to bucket")
		return nil, err
	}
	return s3Client, nil
}

func getClusters(s3client *s3.S3, s3config S3config, nClusters int) ([]string, error) {
	log.Debug().Msg("Reading clusters")
	clusters, err := s3util.ListFolders(s3client, s3config.Bucket, s3config.Prefix, "", maxKeys)
	if err != nil {
		log.Error().Err(err).Msg("error reading clusters list")
		return nil, err
	}
	log.Debug().Int("total clusters", len(clusters)).Msg("Reading clusters")
	return getRandomSubsliceFromSlice(clusters, nClusters), nil
}

func downloadTarball(s3client *s3.S3, s3config S3config, tarBall string) error {
	log.Debug().Str("archive_path", tarBall).Msg("Downloading tarball")
	body, err := s3util.DownloadObject(s3client, s3config.Bucket, tarBall)
	if err != nil {
		log.Error().Err(err).Str("archive_path", tarBall).Msg("Error downloading tarball")
		return err
	}

	if err := writeToPath(tarBall, body); err != nil {
		log.Error().Err(err).Str("archive_path", tarBall).Msg("Error writing tarball")
		return err
	}

	return nil
}

func getNTarBalls(s3client *s3.S3, s3config S3config, cluster string, nTarballs int) (tarBalls []string, err error) {
	log.Debug().Str("cluster", cluster).Msg("Listing tarballs")
	if nTarballs > maxKeys {
		tarBalls, err = s3util.ListBucket(s3client, s3config.Bucket, cluster, "", maxKeys)
		if len(tarBalls) > nTarballs {
			tarBalls = tarBalls[:nTarballs]
		}
	} else {
		tarBalls, _, err = s3util.ListNObjectsInBucket(s3client, s3config.Bucket, cluster, "", "", int64(nTarballs))
	}
	if err != nil {
		return nil, err
	}
	return tarBalls, err
}
