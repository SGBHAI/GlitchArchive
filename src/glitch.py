from PIL import Image
import sys

def encode(file_path, output_image):
    with open(file_path, 'rb') as f:
        data = f.read()
    header = len(data).to_bytes(4, 'big')
    payload = header + data
    padded_len = (len(payload) + 2) // 3 * 3
    payload = payload.ljust(padded_len, b'\x00')
    pixels = [(payload[i], payload[i+1], payload[i+2]) for i in range(0, len(payload), 3)]
    width = int(len(pixels)**0.5) + 1
    height = (len(pixels) + width - 1) // width
    pixels.extend([(0, 0, 0)] * (width * height - len(pixels)))
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(output_image)

def decode(image_path, output_file):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    flat = bytearray()
    for r, g, b in pixels:
        flat.extend((r, g, b))
    length = int.from_bytes(flat[:4], 'big')
    data = flat[4:4+length]
    with open(output_file, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])