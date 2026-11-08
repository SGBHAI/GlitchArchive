import sys
import math
import cv2
import numpy as np
from core import pack_blob, unpack_blob

def encode(file_path, video_path):
    blob = pack_blob(file_path)
    length_prefix = len(blob).to_bytes(4, 'big')
    full_payload = length_prefix + blob
    
    width, height = 320, 240
    frame_bytes = width * height * 3
    total_frames = math.ceil(len(full_payload) / frame_bytes)
    
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    out = cv2.VideoWriter(video_path, fourcc, 30, (width, height), isColor=True)
    
    for f in range(total_frames):
        chunk = full_payload[f * frame_bytes : (f + 1) * frame_bytes]
        chunk = chunk.ljust(frame_bytes, b'\x00')
        frame = np.frombuffer(chunk, dtype=np.uint8).reshape((height, width, 3))
        out.write(frame)
    out.release()

def decode(video_path, output_file):
    cap = cv2.VideoCapture(video_path)
    raw_bytes = bytearray()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        raw_bytes.extend(frame.tobytes())
    cap.release()
    
    payload_len = int.from_bytes(raw_bytes[:4], 'big')
    blob = bytes(raw_bytes[4 : 4 + payload_len])
    
    _, raw = unpack_blob(blob)
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])