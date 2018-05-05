from PIL import Image
import binascii

# Functions from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def encode(text, img):
    textBin = text_to_bits(text)
    print(textBin)
    textSize = len(textBin)
    count = 0
    img.x = img.size[0]
    img.y = img.size[1]
    pixels = img.load()
    for x in range (0, img.x) :
        for y in range (0, img.y) :
            pixBin = bin(pixels[x, y][0])
            if (count < textSize) :
                newPixel = (int(pixBin[:-1] + textBin[count], 2), pixels[x, y][1], pixels[x, y][2])
                count = count + 1
                img.putpixel((x, y), newPixel)
            else :
                newPixel = (int(pixBin[:-1] + '0', 2), pixels[x, y][1], pixels[x, y][2])
                img.putpixel((x, y), newPixel)
    img.save('new.png')
    return

def decode(img):
    text = ''
    decodedtext = ''
    img.x = img.size[0]
    img.y = img.size[1]
    pixels = img.load()
    for x in range (0, img.x) :
        for y in range (0, img.y) :
            text += bin(pixels[x, y][0])[-1:]

    for x in range (0, len(text), 8) :
        charbin = text[x:x+8]
        if (charbin != '00000000') :
            decodedtext += charbin
        else :
            break
    decodedtext = text_from_bits(decodedtext)
    print decodedtext
    return decodedtext

text = "Hello World!"
#img = Image.open('lena.png', 'r')
#encode(text, img)
new = Image.open('new.png', 'r')
decode(new)
