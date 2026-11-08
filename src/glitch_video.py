# src/glitch_video.py
import sys
import math
import cv2
import numpy as np
from core import pack_blob, unpack_blob

def encode(file_path, video_path, fps=30):
    blob = pack_blob(file_path)
    padded_len = (len(blob) + 2) // 3 * 3
    payload = blob.ljust(padded_len, b'\x00')
    
    width, height = 320, 240
    frame_bytes = width * height * 3
    total_frames = math.ceil(len(payload) / frame_bytes)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    
    for f in range(total_frames):
        chunk = payload[f * frame_bytes : (f + 1) * frame_bytes]
        chunk = chunk.ljust(frame_bytes, b'\x00')
        frame = np.frombuffer(chunk, dtype=np.uint8).reshape((height, width, 3))
        out.write(frame)
    
    out.release()

def decode(video_path, output_file):
    cap = cv2.VideoCapture(video_path)
    blob = bytearray()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        blob.extend(frame.tobytes())
    
    cap.release()
    _, raw = unpack_blob(bytes(blob))
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])