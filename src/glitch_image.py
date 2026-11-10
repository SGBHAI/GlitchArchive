import sys
import math
from PIL import Image
from .core import pack_blob, unpack_blob

def encode(file_path, output_image):
    with open(file_path, "rb") as f:
        raw_data = f.read()
    blob = pack_blob(file_path, raw_data)
    padded_len = (len(blob) + 2) // 3 * 3
    payload = blob.ljust(padded_len, b'\x00')
    pixels = [(payload[i], payload[i+1], payload[i+2]) for i in range(0, len(payload), 3)]
    width = int(len(pixels)**0.5) + 1
    height = (len(pixels) + width - 1) // width
    pixels.extend([(0, 0, 0)] * (width * height - len(pixels)))
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(output_image)

def decode(image_path, output_file):
    img = Image.open(image_path)
    flat = bytearray(img.tobytes())
    filename, raw, sha = unpack_blob(bytes(flat))
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])