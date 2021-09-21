from pathlib import Path
from imgopt import convert

OUT_DIR = "out"

# example script to show the usage for optimizing images from a folder

if __name__ == "__main__":
    curdir = Path(".").resolve().parts[-1]
    if curdir == "examples":
        # by doing `python ./image_optimizer`
        images = Path(".").glob("image_optimzer/images/*")
    elif curdir == "image_optimzer":
        # by doing `python ./image_optimizer/__main__.py`
        images = Path(".").glob("images/*")
    else:
        raise "Invalid folder"

    results = []
    for image in images:
        out_image = list(image.parts)
        out_image[-2] = OUT_DIR
        out_image = Path(*out_image)
        convert(str(image), str(out_image))
        results.append((image, out_image))

    # print the difference in size
    print("name     \tin      \tout")
    for (image, out) in results:
        print(
            "{}     \t{} bytes\t{} bytes".format(
                image.name, image.stat().st_size, out.stat().st_size
            )
        )
