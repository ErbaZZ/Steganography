import binascii
import sys

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

def encode(plaintext, image, outimage):
    # Convert plaintext to the binary format
    text_bin = text_to_bits(plaintext)
    # print(text_bin)
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
                    # Replace the last bits of the target pixel with the data bit
                    data_bits = ''
                    for j in range(0, replace_bits):
                        data_bits += text_bin[count] if count < text_size else '0'
                        count += 1
                    colors[i] = int(pix_bin[:-replace_bits] + data_bits, 2)
                else:
                    # Replace the last bits of the target pixel with 0
                    colors[i] = int(pix_bin[:-replace_bits] + '0' * replace_bits, 2)
                i += 1
            image.putpixel((x, y), tuple(colors))
    image.save(outimage)
    print('Image encoded!')
    return


def decode(image):
    text_ = ''
    decoded_text = ''
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    for x in range(0, image.x):
        for y in range(0, image.y):
            # Append data from the image with the last bits of each color channel
            for channel in pixels[x, y]:
                text_ += bin(channel)[-replace_bits:]

    for x in range(0, len(text_), 8):
        # Keep appending data bits until zeroes are found
        char_bin = text_[x:x + 8]
        if char_bin != '00000000':
            decoded_text += char_bin
        else:
            break
    # Convert data bit to plaintext
    decoded_text = text_from_bits(decoded_text)
    return decoded_text


#   TODO: Accept CLI arguments
#       1) python steganography.py -e -p <plaintext> -i <input-image> -o <output-image>
#       2) python steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>
#       3) python steganography.py -d -i <input-encoded-image>                                                  # Print output text to console
#       4) python steganography.py -d -i <input-encoded-image> -o <output-text-file>                            # Save output to file
#   Extra:
#       1) Check image file extension to be only .png and .bmp
#       2) Show warning and instruction when invalid argument pattern is detected

# print 'Number is: ', len(sys.argv), 'arguments.'
# print 'Argument list: ', str(sys.argv)

# Encode
if sys.argv[1] == '-e':
    if len(sys.argv) != 8:
        print('Invalid argument! Please use one of the following formats:')
        print('\tpython steganography.py -e -p <plaintext> -i <input-image> -o <output-image>')
        print('\tpython steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>')
        print('\tpython steganography.py -d -i <input-encoded-image>')
        print('\tpython steganography.py -d -i <input-encoded-image> -o <output-text-file>')
        exit()
    plaintext = ''
    # Get text from file
    if sys.argv[2] == '-f':
        textfile = open(sys.argv[3], 'r')
        for line in textfile:
            plaintext = plaintext + line
    # Get plaintext from cli argument
    elif sys.argv[2] == '-p':
        plaintext = sys.argv[3]

    for i in range(len(sys.argv)):
        # Check input
        if sys.argv[i] == '-i':
            input_image = sys.argv[i + 1]
        # Check output
        if sys.argv[i] == '-o':
            output = sys.argv[i + 1]

    img = Image.open(input_image, 'r')
    encode(plaintext, img, output)

# Decode
elif sys.argv[1] == '-d':
    if len(sys.argv) != 4 and len(sys.argv) != 6:
        print('Invalid argument! Please use one of the following formats:')
        print('\tpython steganography.py -e -p <plaintext> -i <input-image> -o <output-image>')
        print('\tpython steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>')
        print('\tpython steganography.py -d -i <input-encoded-image>')
        print('\tpython steganography.py -d -i <input-encoded-image> -o <output-text-file>')
        exit()
    outflag = False
    for i in range(len(sys.argv)):
        # Check input
        if sys.argv[i] == '-i':
            input_image = sys.argv[i + 1]
        # Check output
        if sys.argv[i] == '-o':
            outflag = True
            output = sys.argv[i + 1]
            f = open(output, "w+")

    img = Image.open(input_image, 'r')
    outtext = decode(img)
    print(outtext)
    if outflag:
        f.write(outtext)
        print('Text saved in a file!')

else:
    print('Invalid argument! Please use one of the following formats:')
    print('\tpython steganography.py -e -p <plaintext> -i <input-image> -o <output-image>')
    print('\tpython steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>')
    print('\tpython steganography.py -d -i <input-encoded-image>')
    print('\tpython steganography.py -d -i <input-encoded-image> -o <output-text-file>')
    exit()
