import zlib
import struct
from pathlib import Path

MAGIC = b"WSTR"

def pack_blob(file_path):
    raw = Path(file_path).read_bytes()
    name = Path(file_path).name.encode()
    compressed = zlib.compress(raw, level=9)
    header = MAGIC + struct.pack(">BIH", len(name), len(compressed), len(raw)) + name
    return header + compressed

def unpack_blob(blob):
    if blob[:4] != MAGIC:
        raise ValueError("Invalid magic bytes")
    name_len, comp_len, _ = struct.unpack(">BIH", blob[4:11])
    name = blob[11:11+name_len].decode()
    compressed = blob[11+name_len:11+name_len+comp_len]
    raw = zlib.decompress(compressed)
    return name, raw