# src/glitch_audio.py
import sys
import math
import wave
from core import pack_blob, unpack_blob

def encode(file_path, audio_path, sample_rate=44100, duration_per_bit=0.01):
    blob = pack_blob(file_path)
    bits = "".join(f"{b:08b}" for b in blob)
    samples_per_bit = int(sample_rate * duration_per_bit)
    
    f0, f1 = 1200, 2400
    audio_data = bytearray()
    
    for bit in bits:
        freq = f1 if bit == '1' else f0
        for i in range(samples_per_bit):
            t = i / sample_rate
            val = int(32767 * math.sin(2 * math.pi * freq * t))
            audio_data.extend(val.to_bytes(2, byteorder='little', signed=True))
    
    with wave.open(audio_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

def decode(audio_path, output_file, sample_rate=44100, duration_per_bit=0.01):
    with wave.open(audio_path, 'r') as wf:
        frames = wf.readframes(wf.getnframes())
    
    samples_per_bit = int(sample_rate * duration_per_bit)
    num_bits = len(frames) // (2 * samples_per_bit)
    bits = []
    
    for b in range(num_bits):
        start = b * samples_per_bit * 2
        end = start + samples_per_bit * 2
        chunk = frames[start:end]
        
        pos_crossings = 0
        for i in range(2, len(chunk), 2):
            prev = int.from_bytes(chunk[i-2:i], byteorder='little', signed=True)
            curr = int.from_bytes(chunk[i:i+2], byteorder='little', signed=True)
            if prev < 0 and curr >= 0:
                pos_crossings += 1
        
        freq = pos_crossings / duration_per_bit
        bits.append('1' if freq > 1800 else '0')
    
    all_bits = "".join(bits)
    byte_array = bytearray()
    for i in range(0, len(all_bits) - 7, 8):
        byte_array.append(int(all_bits[i:i+8], 2))
    
    _, raw = unpack_blob(bytes(byte_array))
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])