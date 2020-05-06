package main

import (
	"bufio"
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
	defer fin.Close()

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
	defer outfile.Close()

	gif.EncodeAll(outfile, &gif.GIF{
		Image: images,
		Delay: delays,
	})
}

func drawAnt(img *image.Paletted, x0 int, y0 int, col int) {
	palette := make(map[int]color.RGBA, 4)
	palette[0] = color.RGBA{200, 100, 100, 255}
	palette[1] = color.RGBA{00, 200, 00, 255}
	palette[2] = color.RGBA{255, 255, 255, 255}
	palette[3] = color.RGBA{105, 62, 200, 255}

	r := image.Rect(x0, y0, x0+10, y0+10)
	draw.Draw(img, r, &image.Uniform{palette[col]}, image.ZP, draw.Src)
}

func drawMarchingAnts(img *image.Paletted, step int) {
	palette := make(map[int]color.RGBA, 1)
	palette[0] = color.RGBA{200, 100, 100, 255}

	for y := 388; y < 510; y += 20 {
		drawAnt(img, 904, y+step, 0)
	}
	for x := 904; x > 798; x -= 20 {
		drawAnt(img, x-step, 530, 0)
	}
	for y := 561; y < 604; y += 20 {
		drawAnt(img, 760, y+step, 1)
	}
	for x := 760; x > 694; x -= 20 {
		drawAnt(img, x-step, 624, 1)
	}
	drawAnt(img, 664+27-10, 616+20-12, 2)
	drawAnt(img, 785, 529, 3)
	drawAnt(img, 786, 530, 3)
}

func main() {
	var images []*image.Paletted
	var delays []int

	steps := 20

	for step := 0; step < steps; step++ {
		img := readOriginal("1.gif")
		drawMarchingAnts(img, step)
		images = append(images, img)
		delays = append(delays, 10)
	}
	writeAnimation("2.gif", images, delays)

}
