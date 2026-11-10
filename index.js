const MAGIC = "WSTR";

function packBlob(name, compressed, raw) {
    const encoder = new TextEncoder();
    const nameBytes = encoder.encode(name);
    const header = new Uint8Array(4 + 1 + 4 + 4 + nameBytes.length);
    header.set([0x57, 0x53, 0x54, 0x52], 0);
    const view = new DataView(header.buffer);
    view.setUint8(4, nameBytes.length);
    view.setUint32(5, compressed.byteLength, false);
    view.setUint32(9, raw.byteLength, false);
    header.set(nameBytes, 13);
    const combined = new Uint8Array(header.byteLength + compressed.byteLength);
    combined.set(header, 0);
    combined.set(new Uint8Array(compressed), header.byteLength);
    return combined;
}

function unpackBlob(buffer) {
    const view = new DataView(buffer);
    const magic = String.fromCharCode(view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3));
    if (magic !== "WSTR") throw new Error("Invalid magic bytes");
    const nameLen = view.getUint8(4);
    const compLen = view.getUint32(5, false);
    const rawLen = view.getUint32(9, false);
    const nameBytes = new Uint8Array(buffer, 13, nameLen);
    const name = new TextDecoder().decode(nameBytes);
    const compressed = buffer.slice(13 + nameLen, 13 + nameLen + compLen);
    return { name, compressed, rawLen };
}