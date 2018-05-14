# Steganography

This script performs steganography to hide plaintext inside a Bitmap or PNG image by converting plaintext into a long string of bits, and hide those bits in the least significant bits of the color channels of the image.

<img src="lena.png" title="Original Image" width="400"> <img src="encoded.png" title="Encoded Image" width="400">

The image on the left is the original image, and the image on the right is the encoded image which contains ~300,000 bytes of text hidden inside generated with the script.

## Getting Started

Please conform to the following instructions to run the script

### Prerequisites

* [Python 3.2+](https://www.python.org/downloads/)
* [Pillow](https://pypi.org/project/Pillow/)

### Installation

Clone the repository
```
git clone https://github.com/ErbaZZ/Steganography
```

#### Linux

Install Python
```
sudo apt-get update
sudo apt-get install Python
```

Install Pillow
```
sudo pip install Pillow
```

#### Windows

Install Python
* Download Python 3 installer from https://www.python.org/downloads/ and run

Install Pillow
```
sudo pip install Pillow
```

## Running

The script can be run in the directory with the script file using one of the following patterns

### Encoding

Encoding plaintext into an image
```
python steganography.py -e -p <plaintext> -i <input-image> -o <output-image>
```
Encoding plaintext from a file into an image
```
python steganography.py -e -f <plaintext-file> -i <input-image> -o <output-image>
```

### Decoding

Decoding plaintext encoded in an image and print it into the console
```
python steganography.py -d -i <input-encoded-image>
```
Decoding plaintext encoded in an image and save the output into a file
```
python steganography.py -d -i <input-encoded-image> -o <output-text-file>
```

### Example

To encode the text in text.txt into lena.png, you can use the following command
```
python steganography.py -e -f text.txt -i lena.png -o encoded.png
```
You will see the following message in the console, and the encoded.png file will be generated in the directory
```
Image encoded!
```
After that, to decode and get the hidden text from the image and save into a file named outtext.txt, you can use the following command
```
python steganography.py -d -i encoded.png -o outtext.txt
```
You will see the following message in the console, and the outtext.txt file will be generated in the directory
```
Text saved in a file!
```

## Authors

* **Weerawat Pawanawiwat** - [ErbaZZ](https://github.com/ErbaZZ)
* **Thatchapon Unprasert** - [PoomSmart](https://github.com/PoomSmart)
* **Dawit Chusetthagarn** - [jeeperror](https://github.com/jeeperror)