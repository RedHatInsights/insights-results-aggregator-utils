package main

type Config struct {
	s3config  S3config
	NClusters int
	NTarballs int
	CSVpath   string
}

type S3config struct {
	AccessKey  string
	SecretKey  string
	Endpoint   string
	Region     string
	DisableSSL bool
	Bucket     string
	Prefix     string
}
