# imgopt

Python library to convert/optimize images. Uses Rust glue to communicate with the mozjpeg, pngquant, webp and svgcleaner.

## Functions

### def convert(str, str):
Convert the input image to the output image. The type is based on the file extension.

```python
# re-encode jpg image using mozjpeg
imgopt.convert("input_image.jpg", "output_image.jpg")

# converts the input jpg image to png
imgopt.convert("input_image.jpg", "output_image.png")
```

### def convert_explicit((str, str), (str, str)):
Convert the input image to the output image. The image type is given as an argument and the file extension is ignored. This can be handy if you are handling temporary files for instance (that dont have file extensions).

```python
imgopt.convert_explicit(("input_image.jpg", imgopt.JPG), ("output_image", imgopt.WEBP))
```

## Constants

### Image formats

```python
import imgopt

imgopt.JPG
imgopt.JPEG
imgopt.PNG
imgopt.SVG
imgopt.WEBP
```