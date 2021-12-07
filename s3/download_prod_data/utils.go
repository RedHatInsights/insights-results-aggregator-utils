package main

import "math/rand"

func getRandomSubsliceFromSlice(slice []string, nElements int) []string {
	for i := range slice {
		j := rand.Intn(i + 1)
		slice[i], slice[j] = slice[j], slice[i]
	}
	if nElements > len(slice) {
		return slice
	} else {
		return slice[:nElements]
	}
}
