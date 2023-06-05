/*
Copyright © 2023 Pavel Tisnovsky

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// This tool generates file named "cluster_names.txt" that will contain
// list of cluster names to be used by producer and consumer (reader).
//
// Format of this file is following:
// 735666f9-c2f8-4152-9156-7cbf6e16a99e
// db041ec6-e483-4fd5-b94d-aa65793715c7
// a62ba439-5f23-4fe9-bc0c-b3b2c4b8def2
// a4156d08-2372-49db-8908-c7240264dbda
// 34dd2a72-78c4-4634-a2b8-e1171e035e53
// 34e1d8c8-c62a-442c-adc7-5205c4c6a171
// 2d75f1dd-32db-479a-ae6a-d30897645bb9
// 53e0c655-d88e-4751-9332-3431580c6355
// bd199701-edf8-43ce-99b4-1ad2c44f7f47
// 1c5a8c1f-2e91-46ad-86be-de093e839230
// etc.
//
// Please note that Unix line ending is used.

package main

import (
	"fmt"
	"log"
	"os"

	"github.com/google/uuid"
)

const uniqueClusterNames = 100

func main() {
	// open output file
	fout, err := os.Create("cluster_names.txt")
	if err != nil {
		log.Fatal(err)
	}

	// close fout on exit and check for its returned error
	defer func() {
		err := fout.Close()

		if err != nil {
			log.Fatal(err)
		}
	}()

	for i := 0; i < uniqueClusterNames; i++ {
		clusterName := uuid.New().String()
		log.Print(clusterName)
		fmt.Fprintf(fout, "%s\n", clusterName)
	}
}
