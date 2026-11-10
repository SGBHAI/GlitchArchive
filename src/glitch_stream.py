import sys
import math
import numpy as np
from PIL import Image
from .core import pack_blob, unpack_blob

def encode(file_path, output_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
    blob = pack_blob(file_path, raw_data)
    row_size = 320 * 3
    remainder = len(blob) % row_size
    if remainder != 0:
        blob += b'\x00' * (row_size - remainder)
    
    width = 320
    height = len(blob) // row_size
    
    arr = np.frombuffer(blob, dtype=np.uint8).reshape((height, width, 3))
    img = Image.fromarray(arr, 'RGB')
    img.save(output_path)

def decode(input_path, output_file):
    img = Image.open(input_path)
    arr = np.array(img)
    flat = arr.tobytes()
    
    filename, raw, sha = unpack_blob(flat)
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])