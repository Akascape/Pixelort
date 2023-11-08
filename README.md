<br />
<div align="center">
  <img src="https://github.com/Akascape/CTkMenuBar/assets/89206401/c8cf8d66-0864-4d0f-8642-ad3758406c56" alt="Logo" width="300" height="330">
  <h2 align="center">Advanced Pixel Sorting application made with customtkinter and python</h2>
</div>

![Screenshot](https://github.com/Akascape/CTkMenuBar/assets/89206401/f71167c0-6434-4d41-912a-fa67d214d66d)

## What is Pixel Sorting?
Pixel sorting is a digital image processing technique that involves isolating a horizontal or vertical line of pixels in an image and sorting their positions based on any number of criteria, such as luminosity, hue, or saturation 1. The result is a glitchy, abstracted image that can be used for artistic purposes. This tool is based on https://github.com/satyarth/pixelsort

## INSTALLATION
- Download the python version:
  
 [<img src="https://img.shields.io/badge/DOWNLOAD-informational?style=flat&logo=python&logoColor=blue&color=eaea4a" width=250 height=50>](https://github.com/Akascape/Pixelort/archive/refs/heads/main.zip)
- Extract the downloaded file
- Install the modules of requirements.txt: `pip install -r requirements.txt`
- Run `pixelort.py`

## FEATURES

- Drag and Drop file support
- Masking feature
- Save/Import Mask
- 6 Pixel Sorting Modes
- Angle and threshold parameters
- Sorting functions
- Image reference mode
- Check version updates
- Export to png/jpg
- One click live render
- Dark/Light themes
- More...

## Immediate Masking Tool
![Screenshot](https://github.com/Akascape/CTkMenuBar/assets/89206401/d188f772-df60-4fc8-8507-9a6b3d22f571)

You can draw the mask of the area where you want the pixel sorting effect

### Modes

Modes             | Description
------------------|------------
`Random`			    | Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using `character length`.
`Edges`				    | Performs an edge detection, which is used to define intervals. 
`Threshold`		  	| Intervals defined by lightness thresholds; only pixels with a lightness between the upper and lower thresholds are sorted.
`Waves`			    	| Intervals are waves of nearly uniform widths. Control width of waves with `character length`.
`Reference`       | Intervals taken from another specified input image. Should be black and white, and the same size as the input image.
`Border`			    | Sort whole rows, only stopping at image borders.


### Sorting Functions

Sorting function  | Description
------------------|------------
`Lightness`       | Sort by the lightness of a pixel according to a HSL representation.
`Hue`             | Sort by the hue of a pixel according to a HSL representation.
`Saturation`      | Sort by the saturation of a pixel according to a HSL representation.
`Intensity`       | Sort by the intensity of a pixel, i.e. the sum of all the RGB values.
`Minimum`         | Sort on the minimum RGB value of a pixel (either the R, G or B).

<p align="center">
<img src="https://capsule-render.vercel.app/api?type=rect&color=timeGradient&height=2"> 
</p>

