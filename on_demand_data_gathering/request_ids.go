package main

import (
	"fmt"
	"math/rand"
	"strconv"
)

func generateTrackerID() string {
	r1 := rand.Uint64()
	r2 := rand.Uint64()
	return strconv.FormatUint(r1, 36) + strconv.FormatUint(r2, 36)
}

func main() {
	for i := 0; i < 100; i++ {
		id := ""
		for len(id) != 26 {
			id = generateTrackerID()
		}
		fmt.Println(id)
	}
}
