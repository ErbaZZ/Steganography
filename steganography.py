import binascii

from PIL import Image

replace_bits = 1  # must be less than 8 and not too high


# Functions from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def text_to_bits(plaintext, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(plaintext.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int_to_bytes(n).decode(encoding, errors)


def int_to_bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


#   TODO: Improved data hiding algorithm for longer text
#       - Encode + decode input to accommodate longer input?
#       - Other

def encode(plaintext, image):
    # convert plain text to the binary format
    text_bin = text_to_bits(plaintext)
    print(text_bin)
    text_size = len(text_bin)
    count = 0
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    for x in range(0, image.x):
        for y in range(0, image.y):
            i = 0
            colors = [0] * 3
            for channel in pixels[x, y]:
                pix_bin = bin(channel)
                if count < text_size:
                    # replace the last bits of the target pixel with the data bit
                    data_bits = ''
                    for j in range(0, replace_bits):
                        data_bits += text_bin[count] if count < text_size else '0'
                        count += 1
                    colors[i] = int(pix_bin[:-replace_bits] + data_bits, 2)
                else:
                    # replace the last bits of the target pixel with 0
                    colors[i] = int(pix_bin[:-replace_bits] + '0' * replace_bits, 2)
                i += 1
            image.putpixel((x, y), tuple(colors))
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
            # append data from the image with the last bits of each color channel
            for channel in pixels[x, y]:
                text_ += bin(channel)[-replace_bits:]

    for x in range(0, len(text_), 8):
        # keep appending data bits until zeroes are found
        char_bin = text_[x:x + 8]
        if char_bin != '00000000':
            decoded_text += char_bin
        else:
            break
    # convert data bit to plain text
    decoded_text = text_from_bits(decoded_text)
    print(decoded_text)
    return decoded_text


#   TODO: Accept CLI arguments
#       1) python steganography.py -e <plaintext> <raw image filename> <encoded image filename>
#       2) python steganography.py -e -f <plaintext filename> <raw image filename> <encoded image filename>
#       3) python steganography.py -d <encoded image filename>                                                  # Print output text to console
#       4) python steganography.py -d -f <encoded image filename> <output text filename>                        # Save output to file
#   Extra:
#       1) Check image file extension to be only .png and .bmp
#       2) Show warning and instruction when invalid argument pattern is detected

text = "Hello World! This is the test of Steganography program."
img = Image.open('lena.png', 'r')
encode(text, img)
new = Image.open('new.png', 'r')
decode(new)
