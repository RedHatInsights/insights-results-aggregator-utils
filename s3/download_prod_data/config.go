package main

import "flag"

func getConfig() Config {
	accessKeyPtr := flag.String("access-key", "", "access key")
	secretKeyPtr := flag.String("secret-key", "", "secret key")
	endpointPtr := flag.String("endpoint", "https://s3.upshift.redhat.com", "endpoint")
	regionPtr := flag.String("region", "us-east-1", "bucket region")
	disableSSLPtr := flag.Bool("disable-ssl", false, "whether to disable SSL or not")
	bucketPtr := flag.String("bucket", "", "bucket name")
	prefixPtr := flag.String("prefix", "", "path to the clusters folders")
	nClustersPtr := flag.Int("n-clusters", 1, "number of clusters")

	flag.Parse()

	return Config{
		s3config: S3config{
			AccessKey:  *accessKeyPtr,
			SecretKey:  *secretKeyPtr,
			Endpoint:   *endpointPtr,
			Region:     *regionPtr,
			DisableSSL: *disableSSLPtr,
			Bucket:     *bucketPtr,
			Prefix:     *prefixPtr,
		},
		NClusters: *nClustersPtr,
	}
}
