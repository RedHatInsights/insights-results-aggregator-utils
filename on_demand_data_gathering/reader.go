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
	"fmt"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
)

// configuration
const (
	redisAddress = "localhost:6379"
	readingDelay = 1000 * time.Millisecond
	clusterName  = "a4d1525e-a56f-4f3f-9451-e5cc628157b4"
)

func main() {
	// construct new Redis client
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
	context := client.Context()

	for {
		iter := client.Scan(context, 0, clusterName+".*", 0).Iterator()
		for iter.Next(context) {
			fmt.Println(iter.Val())
		}
		if err := iter.Err(); err != nil {
			log.Fatal(err)
		}
		time.Sleep(readingDelay)
	}
}
