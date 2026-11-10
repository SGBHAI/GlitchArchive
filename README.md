# GlitchArchive 🚀

A multi-carrier lossless "weird storage" vault engineered to store arbitrary files inside unconventional digital media—including RGB Pixel Matrices, Pixel Streams, and Chess PGN Containers—with bit-perfect SHA-256 validation. Supports up to 4,294,967,295 bytes (4 GB) of files.

## What It Is
GlitchArchive is a data steganography and unconventional storage engine that transforms any arbitrary file into visual or structured carrier formats like PNG images and PGN chess game notation, enabling lossless round-trip recovery across both CLI Python scripts and browser-based web applications.

## How I Built It
- **Core Engine (`core.py`)**: Implements blob packaging and un-packaging using zlib compression and a 45-byte binary header structure tracking magic bytes (`WSTR`), filename length, compressed length, raw length, and the 32-byte cryptographic SHA-256 hash.
- **Carriers**: Built multi-format encoders and decoders including pixel streams, RGB pixel matrices (with explicit `.convert('RGB')` handling for browser-generated RGBA canvas artifacts), and chess PGN Base64 `PayloadData` headers with dynamic timestamps.
- **Web Interface (`index.html`)**: Frontend implementation utilizing JavaScript `DataView` and browser canvas APIs to pack and unpack payloads directly in the browser, matching the binary header specification for seamless interoperability with the Python CLI.

## What Was Hard
- **Header Synchronization**: Aligning the 45-byte binary header across both Python `struct` formatting and JavaScript `DataView` byte offsets to prevent parsing desyncs between CLI and web carriers.
- **Browser RGBA / RGB Interoperability**: Resolving browser canvas exports saving as RGBA which caused CLI decoders to crash on magic bytes, fixed by forcing `.convert('RGB')` across python image and stream processors.
- **Memory & Scale**: Upgrading the file size ceiling and incorporating robust 32-byte SHA-256 cryptographic verification checks post-decompression.

## Header Table (45 Bytes Base Header + Variable Fields)
| Field       | Size (Bytes) | Type / Description                |
| :---        | :---         | :------------------               |
| `MAGIC`     |      4       | Magic bytes (`WSTR`)              |
| `name_len`  |      1       | Length of original filename (`>B`)|
| `comp_len`  |      4       | Compressed payload length (`>I`)  |
| `raw_len`   |      4       | Uncompressed payload length (`>I`)|
| `SHA-256`   |      32      | Cryptographic hash of raw payload |
| `filename`  |   Variable   | UTF-8 encoded original filename   |
| `compressed`|   Variable   | DEFLATE compressed binary data    |

## My Experience and reason for picking this card
When I first learned about steganography, I was in disbelief. It made me wonder how, why, and what it was. So I watched some YouTube videos to understand how it works, and it became one of my 31st projects. (That was a long time ago, and it was just a bare skeleton—none of it is used here.) Later, I saw Hack Club on Instagram and joined a space-related hackathon or program, though I can't remember its name. As soon as I joined, it ended. While searching for another program, I found Crescent and saw this card, which reminded me that I had done something similar before. That's why I picked this card.

## How to Run
- **Python CLI Pack:** `python -m src.core pack <filename>`
- **Python CLI Unpack:** `python -m src.core unpack <carrier>`
- **Web App:** Serve locally with `python -m http.server 8080`, then open in your browser at `http://localhost:8080`.

## Acknowledgments & AI Assistance Disclosure

GlitchArchive was designed, architected, and built as an independent systems and data-encoding project. Generative AI tools (Google Gemini) were used for suggesting updates and assisting in the generation of the `README.md` by giving format tricks like ```(language) then end with ``` etc.