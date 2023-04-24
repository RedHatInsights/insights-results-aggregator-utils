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

package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/go-redis/redis/v8"
)

// configuration
const (
	redisAddress = "localhost:6379"
	readingDelay = 1000 * time.Millisecond

	clusterNamesFilename = "cluster_names.txt"
)

func readClusterNames(filename string) []string {
	clusterNames := []string{}

	fin, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	// close fi on exit and check for its returned error
	defer func() {
		err := fin.Close()
		if err != nil {
			log.Fatal(err)
		}
	}()

	scanner := bufio.NewScanner(fin)
	for scanner.Scan() {
		clusterName := scanner.Text()
		log.Print(clusterName)
		clusterNames = append(clusterNames, clusterName)
	}

	return clusterNames
}

func chooseClusterName(clusterNames []string) string {
	i := rand.Int() % len(clusterNames)
	return clusterNames[i]
}

func main() {
	fmt.Println("Reading cluster names")
	clusterNames := readClusterNames(clusterNamesFilename)

	fmt.Println("Cluster names")
	for _, clusterName := range clusterNames {
		fmt.Println(clusterName)
	}

	// construct new Redis client
	log.Print("Construction Redis client")
	client := redis.NewClient(&redis.Options{
		Addr:     redisAddress,
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	// close Redis client properly at the end
	defer func() {
		err := client.Close()
		if err != nil {
			log.Fatal(err)
		}
	}()

	// retrieve context
	log.Print("Retrieving context for Redis connection")
	context := client.Context()

	log.Print("Starting query loop")

	for {
		// randomly choose one cluster name
		clusterName := chooseClusterName(clusterNames)

		t1 := time.Now()

		// read all keys for all rule hits for given cluster name
		iter := client.Scan(context, 0, clusterName+".*", 0).Iterator()

		// read all values (rule hits)
		for iter.Next(context) {
			key := iter.Val()
			log.Println(key)
			ruleHits := client.Get(context, key)
			log.Println(ruleHits)
		}
		// are we still ok?
		if err := iter.Err(); err != nil {
			log.Fatal(err)
		}

		t2 := time.Now()
		duration := t2.Sub(t1)
		log.Println("Duration", duration)

		time.Sleep(readingDelay)

		log.Println()
	}
}
