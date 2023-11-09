# Documentation 

## Importing a file

There are 2 ways to import a image file:
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/60741065-65a5-4cad-8c5b-57a6e978c683)

## SETTINGS 

There are 6 modes of pixel sorting

### Common Parameters
  
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/e434e1f9-c7af-4eff-beb5-d7c311f68c52)

### Mode based Parameters

Modes             | Description
------------------|------------
`Random`			    | Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using `character length`.
`Edges`				    | Performs an edge detection, which is used to define intervals. Width can be adjusted with `lower` threshold slider.
`Threshold`		  	| Intervals defined by lightness thresholds; only pixels with a lightness between the `upper` and `lower` thresholds are sorted.
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

### Reference Mode 

![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/89185a86-bb34-46ac-8c62-e7602b8cbfc4)

- `Import Reference Image`: select the reference image from where the intervals will be taken, (drag and drop is also supported in that region)
- `Clean Edges`: Intevals defined by performing edge detection on the reference file.

**The reference image size should match with the imported image!**

## Masking
Masking helps you to achieve the pixel sorting effect in a specific region of image.

- Drawing a mask of imported image:
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/51bc4700-2ed6-4d04-92e1-c0c4fb355ca1)
### Masking Window
![Screenshot 2023-11-09 140102](https://github.com/Akascape/Pixelort/assets/89206401/ae14ec37-3518-457e-a289-75b611ad7f7e)
(Control+Z supported, right click to switch tools)
### Result
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/1561d319-2a23-48aa-9091-543e63017775)


**You can also import a saved mask, and remove the mask:**
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/b8cd6c7a-1072-48e6-8bdf-f90d818da65f)

### Other Options
You can reset all settings and toggle themes, in the help section you can **check for updates** and open documentation.

## Export
![Screenshot](https://github.com/Akascape/Pixelort/assets/89206401/0ce3d1ba-7e34-4a38-a26f-e3ed20572408)

- `PNG`: Save the output image with RGBA configurarion (transparency included)
- `JPG`: Save the output image with RGB configuration (no transparency)


## Other Features
- You can double click on the image for live rendering
- You can also press <SpaceBar> to render the image
- You can press <Esc> key to force quit the application
- You can scroll up/down in the image to zoom

### That's all, enjoy experimenting...
