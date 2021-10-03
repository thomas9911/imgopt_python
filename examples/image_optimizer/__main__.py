import os
from pathlib import Path

try:
    from imgopt import convert
except ModuleNotFoundError as e:
    print("imgopt not found, run the ./build.sh script or install via pip")
    print()
    raise e

# flags
OUT_DIR = "out"
DELETE_OUT_IMAGES = True
ADD_WEBP = True

"""
example script to show the usage for optimizing images from a folder
"""

if __name__ == "__main__":
    curdir = Path(".").resolve().parts[-1]
    if curdir == "examples":
        # by doing `python ./image_optimizer`
        images = Path(".").glob("image_optimizer/images/*")
    elif curdir == "image_optimizer":
        # by doing `python ./image_optimizer/__main__.py`
        images = Path(".").glob("images/*")
    elif curdir == "imgopt_python":
        # by doing `python ./examples/image_optimizer`
        images = Path(".").glob("examples/image_optimizer/images/*")
    else:
        raise "Invalid folder"

    results = []
    for image in images:
        out_image = list(image.parts)
        out_image[-2] = OUT_DIR
        out_image = Path(*out_image)
        convert(str(image), str(out_image))
        if ADD_WEBP:
            webp_out = out_image.with_suffix(".webp")
            convert(str(image), str(webp_out))
            results.append((image, out_image, webp_out))
        else:
            results.append((image, out_image))

    # print the difference in size
    if ADD_WEBP:
        print("name     \tin      \tout      \twebp")
    else:
        print("name     \tin      \tout")

    for result in results:
        if ADD_WEBP:
            print(
                "{}     \t{} bytes\t{} bytes\t{} bytes".format(
                    result[0].name,
                    result[0].stat().st_size,
                    result[1].stat().st_size,
                    result[2].stat().st_size,
                )
            )
        else:
            print(
                "{}     \t{} bytes\t{} bytes".format(
                    result[0].name, result[0].stat().st_size, result[1].stat().st_size
                )
            )

        if DELETE_OUT_IMAGES:
            os.remove(result[1])
        if DELETE_OUT_IMAGES and ADD_WEBP:
            os.remove(result[2])
