# On Demand Data Gathering benchmarks

Simple benchmark that check how performant is Redis when multiple rule hits are
stored in its in-memory database in case append only log (AOL) is enabled.  The
benchmark consists of three tools:

## `cluster_names.go`

This tool generates file named "cluster_names.txt" that will contain
list of cluster names to be used by producer and consumer (reader).
Need to be started before benchmarks.

## `publisher.go`

This tool start producing (storing) rule hits into Redis with frequency defined
by recordingDelay value. Multiple rule hits can be stored for given cluster
which means that On Demand Data Gathering functionality can be simulated by this
tool.

Can be started independently to `reader.go`

## `reader.go`

This tool periodically try to retrieve rule hits from Redis storage.
If there are multiple results (rule hits) for given cluster, all rule hits
are read and displayed on console. Additionally file named "query_times.txt"
is created and filled in with query times.

Can be started independently to `publisher.go`
