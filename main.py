from PIL import Image
import bisect

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


def run():
    filename = 'morgan2.png'
    existing_image = Image.open(filename)

    gray_image = existing_image.convert(mode='L')
    width, height = gray_image.size
    output_image = Image.new('L', (width*128, height*128))

    for i in range(1, width - 1):
        for j in range(1, height - 1):
            quantize_image, pixel = quantize(gray_image.getpixel((i, j)))
            gray_image.putpixel((i, j), pixel)
            output_image.paste(quantize_image, box=(i*128, j*128))

    #gray_image.rotate(90)
    #gray_image.show()
    #output_image.show()
    output_image.save("output.png")
    #new_image.save("output.png")


def quantize(pixel_value):
    index = bisect.bisect_right(midpoints, pixel_value)
    if index >= num_sections - 1:
        index = num_sections - 1
    return die_map.get(index), midpoints[index]


if __name__ == '__main__':
    run()
