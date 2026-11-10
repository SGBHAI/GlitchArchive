const MAGIC = new TextEncoder().encode("WSTR");

async function sha256(buffer) {
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

function packBlob(filename, rawData) {
    const nameBytes = new TextEncoder().encode(filename);
    if (nameBytes.length > 255) throw new Error("Filename exceeds 255 bytes");
    
    const compressed = pako.deflate(rawData);
    const header = new ArrayBuffer(13);
    const view = new DataView(header);
    
    MAGIC.forEach((b, i) => view.setUint8(i, b));
    view.setUint8(4, nameBytes.length);
    view.setUint32(5, compressed.length, false);
    view.setUint32(9, rawData.length, false);
    
    const result = new Uint8Array(13 + nameBytes.length + compressed.length);
    result.set(new Uint8Array(header), 0);
    result.set(nameBytes, 13);
    result.set(compressed, 13 + nameBytes.length);
    return result;
}

async function unpackBlob(blob) {
    const view = new DataView(blob.buffer, blob.byteOffset, blob.byteLength);
    for (let i = 0; i < 4; i++) {
        if (view.getUint8(i) !== MAGIC[i]) throw new Error("Invalid magic bytes");
    }
    
    const nameLen = view.getUint8(4);
    const compLen = view.getUint32(5, false);
    const rawLen = view.getUint32(9, false);
    
    const nameEnd = 13 + nameLen;
    const filename = new TextDecoder().decode(blob.subarray(13, nameEnd));
    const compressed = blob.subarray(nameEnd, nameEnd + compLen);
    const rawData = pako.inflate(compressed);
    
    const hash = await sha256(rawData);
    return { filename, rawData, hash };
}