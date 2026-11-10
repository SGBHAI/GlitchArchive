import struct
import zlib
import hashlib
import sys

MAGIC = b"WSTR"

def pack_blob(filename: str, raw_data: bytes) -> bytes:
    name_bytes = filename.encode("utf-8")
    if len(name_bytes) > 255:
        raise ValueError("Filename exceeds 255 bytes")
    compressed = zlib.compress(raw_data)
    file_hash = hashlib.sha256(raw_data).digest()
    header = struct.pack(">BII", len(name_bytes), len(compressed), len(raw_data))
    return MAGIC + header + file_hash + name_bytes + compressed

def unpack_blob(blob: bytes):
    if not blob.startswith(MAGIC):
        raise ValueError("Invalid magic bytes")
    name_len, comp_len, raw_len = struct.unpack(">BII", blob[4:13])
    stored_hash = blob[13:45]
    name_end = 45 + name_len
    filename = blob[45:name_end].decode("utf-8")
    compressed = blob[name_end:name_end + comp_len]
    raw_data = zlib.decompress(compressed)
    computed_hash = hashlib.sha256(raw_data).digest()
    if computed_hash != stored_hash:
        raise ValueError("SHA-256 integrity check failed!")
    return filename, raw_data, stored_hash.hex()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    action = sys.argv[1]
    target = sys.argv[2]
    if action == "pack":
        with open(target, "rb") as f:
            data = f.read()
        packed = pack_blob(target, data)
        with open(target + ".wstr", "wb") as f:
            f.write(packed)
    elif action == "unpack":
        with open(target, "rb") as f:
            data = f.read()
        fname, raw, sha = unpack_blob(data)
        with open(fname, "wb") as f:
            f.write(raw)