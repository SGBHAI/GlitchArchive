import zlib
import struct
from pathlib import Path

MAGIC = b"WSTR"

def pack_blob(file_path):
    raw = Path(file_path).read_bytes()
    name = Path(file_path).name.encode()
    if len(name) > 255:
        raise ValueError("Filename exceeds 255 bytes limit")
    compressed = zlib.compress(raw, level=9)
    header = MAGIC + struct.pack(">BII", len(name), len(compressed), len(raw)) + name
    return header + compressed

def unpack_blob(blob):
    if blob[:4] != MAGIC:
        raise ValueError("Invalid magic bytes")
    name_len, comp_len, _ = struct.unpack(">BII", blob[4:13])
    name = blob[13:13+name_len].decode()
    compressed = blob[13+name_len:13+name_len+comp_len]
    raw = zlib.decompress(compressed)
    return name, raw