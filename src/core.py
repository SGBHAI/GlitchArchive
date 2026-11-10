import struct
import zlib
import hashlib

MAGIC = b"WSTR"

def pack_blob(filename: str, raw_data: bytes) -> bytes:
    name_bytes = filename.encode("utf-8")
    if len(name_bytes) > 255:
        raise ValueError("Filename exceeds 255 bytes")
    compressed = zlib.compress(raw_data)
    header = struct.pack(">BII", len(name_bytes), len(compressed), len(raw_data))
    return MAGIC + header + name_bytes + compressed

def unpack_blob(blob: bytes):
    if not blob.startswith(MAGIC):
        raise ValueError("Invalid magic bytes")
    name_len, comp_len, raw_len = struct.unpack(">BII", blob[4:13])
    name_end = 13 + name_len
    filename = blob[13:name_end].decode("utf-8")
    compressed = blob[name_end:name_end + comp_len]
    raw_data = zlib.decompress(compressed)
    
    expected_hash = hashlib.sha256(raw_data).hexdigest()
    return filename, raw_data, expected_hash