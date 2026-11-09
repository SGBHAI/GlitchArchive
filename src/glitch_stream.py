import sys
import math
import numpy as np
from PIL import Image
from core import pack_blob, unpack_blob

def encode(file_path, output_path):
    blob = pack_blob(file_path)
    padded_len = math.ceil(len(blob) / 3) * 3
    payload = bytearray(padded_len)
    payload[:len(blob)] = blob
    
    width = 320
    num_pixels = len(payload) // 3
    height = math.ceil(num_pixels / width)
    
    arr = np.frombuffer(payload, dtype=np.uint8).reshape((height, width, 3))
    img = Image.fromarray(arr, 'RGB')
    img.save(output_path)

def decode(input_path, output_file):
    img = Image.open(input_path)
    arr = np.array(img)
    flat = arr.tobytes()
    
    _, raw = unpack_blob(flat)
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])