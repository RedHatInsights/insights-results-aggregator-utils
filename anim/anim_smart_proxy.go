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

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/gif"
	"os"
)

func readOriginal(filename string) *image.Paletted {
	fin, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer func() {
		err := fin.Close()
		if err != nil {
			panic(err)
		}
	}()

	reader := bufio.NewReader(fin)

	img, err := gif.Decode(reader)
	if err != nil {
		panic(err)
	}
	return img.(*image.Paletted)
}

func writeAnimation(filename string, images []*image.Paletted, delays []int) {
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer func() {
		err := outfile.Close()
		if err != nil {
			panic(err)
		}
	}()

	err = gif.EncodeAll(outfile, &gif.GIF{
		Image: images,
		Delay: delays,
	})
	if err != nil {
		panic(err)
	}
}

func drawAnt(img *image.Paletted, x0 int, y0 int, col int) {
	palette := make(map[int]color.RGBA, 4)
	palette[0] = color.RGBA{0, 0, 0, 255}
	palette[1] = color.RGBA{0, 146, 0, 255}
	palette[2] = color.RGBA{182, 0, 0, 255}

	r1 := image.Rect(x0-8, y0-8, x0+8, y0+8)
	draw.Draw(img, r1, &image.Uniform{palette[0]}, image.ZP, draw.Src)

	r2 := image.Rect(x0-7, y0-7, x0+7, y0+7)
	draw.Draw(img, r2, &image.Uniform{palette[col]}, image.ZP, draw.Src)
}

const Step = 2
const Delay = 5

func main() {
	var images []*image.Paletted
	var delays []int

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

	for _, path := range paths {
		fmt.Println(path)
		x1 := path[0]
		y1 := path[1]
		x2 := path[2]
		y2 := path[3]
		color := path[4]

		x3 := path[5]
		y3 := path[6]
		color3 := path[7]

		x4 := path[8]
		y4 := path[9]
		color4 := path[10]

		xd := 0
		yd := 0
		steps := 0

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

		for i := 0; i < steps; i += Step {
			img := readOriginal("Smart proxy architecture.gif")
			drawAnt(img, x1, y1, color)
			if x3 >= 0 && y3 >= 0 {
				drawAnt(img, x3, y3, color3)
			}
			if x4 >= 0 && y4 >= 0 {
				drawAnt(img, x4, y4, color4)
			}
			images = append(images, img)
			delays = append(delays, Delay)
			x1 += xd
			y1 += yd
		}
	}

	images = append(images, readOriginal("Smart proxy architecture.gif"))
	delays = append(delays, 200)

	writeAnimation("anim.gif", images, delays)

}
