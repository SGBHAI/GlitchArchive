import sys
import math
import cv2
import numpy as np
from core import pack_blob, unpack_blob

def encode(file_path, video_path, fps=30):
    blob = pack_blob(file_path)
    # Store exact length prefix (4 bytes) before payload so decoder knows where valid data ends
    length_prefix = len(blob).to_bytes(4, 'big')
    full_payload = length_prefix + blob
    
    padded_len = (len(full_payload) + 2) // 3 * 3
    payload = full_payload.ljust(padded_len, b'\x00')
    
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
    raw_bytes = bytearray()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        raw_bytes.extend(frame.tobytes())
    
    cap.release()
    
    if len(raw_bytes) < 4:
        raise ValueError("Video file too short or empty")
        
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