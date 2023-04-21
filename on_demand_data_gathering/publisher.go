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
	"encoding/json"
	"log"
	"math/rand"
	"strconv"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
)

// configuration
const (
	redisAddress   = "localhost:6379"
	recordDuration = "10s"
	recordingDelay = 1500 * time.Millisecond
	minRuleHits    = 1
	maxRuleHits    = 10
)

type RuleHit struct {
	RuleFQDN  string
	ErrorKey  string
	TotalRisk uint
}

var ruleHits = []RuleHit{
	RuleHit{
		"nodes_requirements_check",
		"NODES_MINIMUM_REQUIREMENTS_NOT_MET",
		2,
	},
	RuleHit{
		"bug_1234567",
		"BUGZILLA_BUG_1234567",
		1,
	},
	RuleHit{
		"bug_5678900",
		"BUGZILLA_BUG_5678900",
		2,
	},
	RuleHit{
		"bug_9999999",
		"BUGZILLA_BUG_9999999",
		2,
	},
	RuleHit{
		"nodes_kubelet_version_check",
		"NODE_KUBELET_VERSION",
		3,
	},
	RuleHit{
		"samples_op_failed_image_import_check",
		"SAMPLES_FAILED_IMAGE_IMPORT_ERR",
		0},
	RuleHit{
		"cluster_wide_proxy_auth_check",
		"AUTH_OPERATOR_PROXY_ERROR",
		3,
	},
	RuleHit{
		"image_registry_pv_not_bound",
		"MISSING_REQUIREMENTS",
		5,
	},
}

func generateRuleHits() []RuleHit {
	// construct slice with required capacity first
	hitsCount := minRuleHits + rand.Int()%maxRuleHits
	hits := make([]RuleHit, hitsCount)

	// add random rule hits into the slice
	// (hits will be repeated, but we don't care at this moment)
	for i := 0; i < hitsCount; i++ {
		hits[i] = ruleHits[rand.Int()%len(ruleHits)]
	}
	return hits
}

func generateRecord() string {
	ruleHits := generateRuleHits()
	asJSON, err := json.MarshalIndent(ruleHits, "", "\t")
	if err != nil {
		log.Fatal(err)
	}
	return string(asJSON)
}

func generateClusterName() string {
	return uuid.New().String()
}

func generateTrackerID() string {
	r1 := rand.Uint64()
	r2 := rand.Uint64()
	return strconv.FormatUint(r1, 36) + strconv.FormatUint(r2, 36)
}

func generateReportKey() string {
	return generateClusterName() + "." + generateTrackerID()
}

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

	expiration, err := time.ParseDuration(recordDuration)
	if err != nil {
		log.Fatal(err)
	}

	// write records to database continuously
	for {
		// generate report
		key := generateReportKey()
		record := generateRecord()

		// write one record to database
		err = client.Set(context, key, record, expiration).Err()
		log.Println("Generated report for key", key)

		// check for error
		if err != nil {
			log.Fatal(err)
		}

		time.Sleep(recordingDelay)
	}

}
