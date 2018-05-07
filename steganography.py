import binascii

from PIL import Image


# Functions from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def text_to_bits(plaintext, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(plaintext.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def encode(plaintext, image):
    text_bin = text_to_bits(plaintext)
    print(text_bin)
    text_size = len(text_bin)
    count = 0
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    for x in range(0, image.x):
        for y in range(0, image.y):
            pix_bin = bin(pixels[x, y][0])
            if count < text_size:
                new_pixel = (int(pix_bin[:-1] + text_bin[count], 2), pixels[x, y][1], pixels[x, y][2])
                count = count + 1
                image.putpixel((x, y), new_pixel)
            else:
                new_pixel = (int(pix_bin[:-1] + '0', 2), pixels[x, y][1], pixels[x, y][2])
                image.putpixel((x, y), new_pixel)
    image.save('new.png')
    return


def decode(image):
    text_ = ''
    decoded_text = ''
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    for x in range(0, image.x):
        for y in range(0, image.y):
            text_ += bin(pixels[x, y][0])[-1:]

    for x in range(0, len(text_), 8):
        char_bin = text_[x:x + 8]
        if char_bin != '00000000':
            decoded_text += char_bin
        else:
            break
    decoded_text = text_from_bits(decoded_text)
    print(decoded_text)
    return decoded_text


text = "Hello World!"
# img = Image.open('lena.png', 'r')
# encode(text, img)
new = Image.open('new.png', 'r')
decode(new)
