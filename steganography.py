import sys
from PIL import Image

# Functions from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def print_usage():
    print('Invalid argument! Please use one of the following formats:')
    print('\tpython steganography.py -e -p <plaintext> -i <input-image> -o <output-image>')
    print('\tpython steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>')
    print('\tpython steganography.py -d -i <input-encoded-image>')
    print('\tpython steganography.py -d -i <input-encoded-image> -o <output-text-file>')
    exit()

def encode(plaintext, image, outimage):
    # Convert plaintext to the binary format
    text_bin = text_to_bits(plaintext)
    # print(text_bin)
    text_size = len(text_bin)
    count = 0
    endencode = 0
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    for sub_position in range(1, 8):
        if endencode >= 8:
            break
        for x in range(0, image.x):
            if endencode >= 8:
                break
            for y in range(0, image.y):
                if endencode >= 8:
                    break
                i = 0
                colors = [0] * 3
                for channel in pixels[x, y]:
                    pix_bin = bin(channel)[2:].zfill(8)
                    if count < text_size:
                        # Replace the bit of the target pixel with the data bit
                        colors[i] = int(pix_bin[:-sub_position] + text_bin[count] + pix_bin[9 - sub_position:], 2)
                        count += 1
                    else:
                        # Replace the bit of the target pixel with 0
                        colors[i] = int(pix_bin[:-sub_position] + '0' + pix_bin[9 - sub_position:], 2)
                        endencode += 1

                    i += 1
                image.putpixel((x, y), tuple(colors))
    image.save(outimage)
    print('Image encoded!')
    return

def decode(image):
    text_bin = ''
    decoded_text = ''
    image.x = image.size[0]
    image.y = image.size[1]
    pixels = image.load()
    enddecode = 0
    for pos in range(0, 8):
        if enddecode >= 8 and len(text_bin) % 8 == 0:
            break
        for x in range(0, image.x):
            if enddecode >= 8 and len(text_bin) % 8 == 0:
                break
            for y in range(0, image.y):
                if enddecode >= 8 and len(text_bin) % 8 == 0:
                    break
                # Append data from the image with the bits of each color channel
                for channel in pixels[x, y]:
                    bit = bin(channel)[2:].zfill(8)[7 - pos:8 - pos]
                    text_bin += bit
                    if str(bit) == '0':
                        enddecode += 1
                    else:
                        enddecode = 0

    for x in range(0, len(text_bin), 8):
        # Keep appending data bits until zeroes are found
        char_bin = text_bin[x:x + 8]
        if char_bin != '00000000':
            decoded_text += char_bin
        else:
            break
    # Convert data bit to plaintext
    decoded_text = text_from_bits(decoded_text)
    return decoded_text

# Encode
if len(sys.argv) <= 1:
    print_usage()
elif sys.argv[1] == '-e':
    if len(sys.argv) != 8:
        print_usage()
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
        print_usage()
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

    if outflag:
        f.write(outtext)
        print('Text saved in a file!')
    else:
        print(outtext)

else:
    print_usage()