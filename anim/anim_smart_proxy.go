/*
Copyright © 2020 Pavel Tisnovsky

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

// Creates animation based on static GIF image + set of programmed rules. That
// animation displays data flow between Insights Results Smart Proxy and other
// services (internal and external ones).

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/gif"
	"os"
)

// readOriginal function tries to read the GIF file that contains the static
// input image. Animation to be created are based on this source image.
func readOriginal(filename string) *image.Paletted {
	// try to open the file specified by its name and check for any error
	fin, err := os.Open(filename)
	if err != nil {
		panic(err)
	}

	// file needs to be closed properly before that function ends
	defer func() {
		// try to close the file and check for any error that might
		// happened
		err := fin.Close()
		if err != nil {
			panic(err)
		}
	}()

	reader := bufio.NewReader(fin)

	// try to decode GIF frames from reader
	img, err := gif.Decode(reader)
	if err != nil {
		panic(err)
	}

	// we have to use image.Paletted, so it is needed to convert the image
	// into desired format
	return img.(*image.Paletted)
}

// writeAnimation function stores all images into GIF file. Each image (from
// `images` parameter) is stored as a GIF frame and delays between frames are
// provided by `delays` parameter. Please note that it would be possible to
// create smaller GIF image by applying external tool like `gifsicle` to the
// generated GIF file.
func writeAnimation(filename string, images []*image.Paletted, delays []int) {
	// try to open the file specified by its name and check for any error
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}

	// file needs to be closed properly before that function ends
	defer func() {
		// try to close the file and check for any error that might
		// happened
		err := outfile.Close()
		if err != nil {
			panic(err)
		}
	}()

	// try to encode all GIF frames to output file
	err = gif.EncodeAll(outfile, &gif.GIF{
		Image: images,
		Delay: delays,
	})

	//  check if any error occured during EncodeAll operation
	if err != nil {
		panic(err)
	}
}

// drawAnt function draws one "marching" ant into the frame represented by
// `img` parameter. Position (center of ant) of marching ant is specified by
// `x0` and `y0`, and the color is selected by `col` parameter. There are four
// colors that can be used.
//
// TODO: make color palette completely configurable
func drawAnt(img *image.Paletted, x0 int, y0 int, col int) {
	// standard color palette with three colors
	palette := make(map[int]color.RGBA, 4)

	// initialize color palette
	palette[0] = color.RGBA{0, 0, 0, 255}
	palette[1] = color.RGBA{0, 146, 0, 255}
	palette[2] = color.RGBA{182, 0, 0, 255}

	// rectangle that represents the ant
	r1 := image.Rect(x0-8, y0-8, x0+8, y0+8)

	// draw rectangle using the first color (black)
	draw.Draw(img, r1, &image.Uniform{palette[0]}, image.ZP, draw.Src)

	// rectangle that represents the ant
	r2 := image.Rect(x0-7, y0-7, x0+7, y0+7)

	// draw rectangle using the selected color
	draw.Draw(img, r2, &image.Uniform{palette[col]}, image.ZP, draw.Src)
}

const Step = 2
const Delay = 5

// main function is called by runtime after the tool has been started.
func main() {
	// frames representing the whole animation stored in GIF file
	var images []*image.Paletted

	// delays between frames
	var delays []int

	// paths with additional attributes
	paths := [][]int{
		{1144, 200, 1086, 200, 1, -1, -1, 0, -1, -1, 0},
		{1086, 200, 1086, 329, 1, -1, -1, 0, -1, -1, 0},
		{1086, 329, 1050, 329, 1, -1, -1, 0, -1, -1, 0},

		{1006, 287, 1006, 204, 1, 1050, 329, 1, -1, -1, 0},
		{1006, 204, 914, 204, 1, 1050, 329, 1, -1, -1, 0},

		{914, 204, 1006, 204, 2, 1050, 329, 1, -1, -1, 0},
		{1006, 204, 1006, 287, 2, 1050, 329, 1, -1, -1, 0},

		{1006, 373, 1006, 445, 1, 1050, 329, 1, 1006, 287, 2},
		{1006, 445, 914, 445, 1, 1050, 329, 1, 1006, 287, 2},

		{914, 445, 1006, 445, 2, 1050, 329, 1, 1006, 287, 2},
		{1006, 445, 1006, 373, 2, 1050, 329, 1, 1006, 287, 2},

		{1050, 329, 1086, 329, 2, -1, -1, 0, -1, -1, 0},
		{1086, 329, 1086, 200, 2, -1, -1, 0, -1, -1, 0},
		{1086, 200, 1144, 200, 2, -1, -1, 0, -1, -1, 0},
	}

	// draw ants animation along the paths
	for _, path := range paths {
		fmt.Println(path)
		// basic parameter for moving ant
		x1 := path[0]
		y1 := path[1]
		x2 := path[2]
		y2 := path[3]
		color := path[4]

		// special point at end
		x3 := path[5]
		y3 := path[6]
		color3 := path[7]

		// special point at end
		x4 := path[8]
		y4 := path[9]
		color4 := path[10]

		// ant move vector
		xd := 0
		yd := 0
		steps := 0

		// calculate the move vector
		if x1 == x2 {
			fmt.Println("vertical")
			if y1 < y2 {
				yd = Step
				steps = y2 - y1
			} else {
				yd = -Step
				steps = y1 - y2
			}
		} else {
			fmt.Println("horizontal")
			if x1 < x2 {
				xd = Step
				steps = x2 - x1
			} else {
				xd = -Step
				steps = x1 - x2
			}
		}

		// create animation for the active path
		for i := 0; i < steps; i += Step {
			// read original image
			// TODO: make the file name configurable
			img := readOriginal("Smart proxy architecture.gif")
			drawAnt(img, x1, y1, color)

			// first special block
			if x3 >= 0 && y3 >= 0 {
				drawAnt(img, x3, y3, color3)
			}

			// second special block
			if x4 >= 0 && y4 >= 0 {
				drawAnt(img, x4, y4, color4)
			}
			// add frame into set of frames
			images = append(images, img)
			delays = append(delays, Delay)
			x1 += xd
			y1 += yd
		}
	}

	// last image is the same as the original one with long delay
	images = append(images, readOriginal("Smart proxy architecture.gif"))
	delays = append(delays, 200)

	// write resulting animation (set of frames) into GIF file
	// TODO: make the file name configurable
	writeAnimation("anim.gif", images, delays)
}
