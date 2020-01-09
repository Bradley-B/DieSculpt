from PIL import Image
import PIL.ImageOps
import bisect
import tkinter
from tkinter.filedialog import askopenfilename
import os

die_image_dimension = 42
num_sections = 6
base = 255 / num_sections
midpoints = list(map(lambda x: int(x * base), range(1, num_sections + 1)))

die_map = {
    0: 'dice-face-one.png',
    1: 'dice-face-two.png',
    2: 'dice-face-three.png',
    3: 'dice-face-four.png',
    4: 'dice-face-five.png',
    5: 'dice-face-six.png'
}

for key, val in die_map.items():
    die_map[key] = Image.open(val)
    die_map[key] = die_map[key].convert(mode='L')
    die_map[key] = PIL.ImageOps.invert(die_map[key])


def run():
    tkinter.Tk().withdraw()
    filename = askopenfilename()
    existing_image = Image.open(filename)

    gray_image = existing_image.convert(mode='L')
    width, height = gray_image.size
    output_image = Image.new('L', (width*die_image_dimension, height*die_image_dimension), color=150)

    for i in range(0, width):
        for j in range(0, height):
            quantize_image, pixel = quantize(gray_image.getpixel((i, j)))
            # gray_image.putpixel((i, j), pixel)
            output_image.paste(quantize_image, box=(i*die_image_dimension, j*die_image_dimension))

    output_image.show()
    if not os.path.exists("output"):
        os.makedirs("output")
    output_image.save("output/output_" + os.path.basename(filename))


def quantize(pixel_value):
    index = bisect.bisect_right(midpoints, pixel_value)
    if index >= num_sections - 1:
        index = num_sections - 1
    return die_map.get(num_sections-index-1), midpoints[index]


if __name__ == '__main__':
    run()
