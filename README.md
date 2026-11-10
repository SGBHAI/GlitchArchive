# GlitchArchive 🚀

A multi-carrier lossless "weird storage" vault engineered to store arbitrary files inside unconventional digital media—including RGB Pixel Matrices, Pixel Streams, and Chess PGN Containers—with bit-perfect SHA-256 validation. Supports up to 4,294,967,295 bytes (4 GB) of files.

## What It Is
GlitchArchive is a data steganography and unconventional storage engine that transforms any arbitrary file into visual or structured carrier formats like PNG images and PGN chess game notation, enabling lossless round-trip recovery across both CLI Python scripts and browser-based web applications.

## How I Built It
- **Core Engine (`core.py`)**: Implements blob packaging and un-packaging using zlib compression and a 13-byte binary header structure (`>BII`) tracking magic bytes (`WSTR`), filename length, compressed length, and raw length.
- **Carriers**: Built multi-format encoders and decoders including pixel streams, RGB pixel matrices, and chess PGN move converters.
- **Web Interface (`index.html`)**: Frontend implementation utilizing JavaScript `DataView` and browser canvas APIs to pack and unpack payloads directly in the browser, matching the 13-byte binary header specification for seamless interoperability with the Python CLI.

## What Was Hard
- **Header Synchronization**: Aligning the 13-byte binary header (`>BII`) across both Python `struct` formatting and JavaScript `DataView` byte offsets (`Uint8` and big-endian `Uint32`) to prevent parsing desyncs between CLI and web carriers.
- **Memory & Scale**: Upgrading the file size ceiling from 64 KB (`H` 16-bit short) to 4 GB (`I` 32-bit uint) without corrupting compressed stream offsets or breaking byte-level SHA-256 integrity checks.

## Header Table (13 Bytes Total)
| Field      | Type / Size         | Description                          |
| :---       | :------             |                                      |  
| **Magic**  | 4 Bytes (`b"WSTR"`) | File signature identifier            |
| **NameLen**| 1 Byte (`uint8`)    | Length of the original filename      |
| **CompLen**| 4 Bytes (`uint32be`)| Length of the zlib compressed payload|
| **RawLen** | 4 Bytes (`uint32be`)| Length of the uncompressed raw data  |
| **Name**   | `NameLen` Bytes     | UTF-8 encoded filename string        |
| **Payload**| `CompLen` Bytes     | Zlib-compressed binary data          |

## My Experience and reason for picking this card
When I first learned about the idea of steganography, I was in disbelief—it made me wonder how, why, and what. So I watched some YouTube videos to understand how it works, and then it became one of my 31st projects (that was a long time ago). Later, I saw Hack Club on Instagram and joined a space-related hackathon or program, though I can't remember the name. As soon as I joined, it ended. While searching for another program, I found Crescent and saw this card, which reminded me that I had done something similar before. That's why I picked this card.

## How to Run
- **Python CLI Pack:** `python -m src.core pack <filename>`
- **Python CLI Unpack:** `python -m src.core unpack <carrier>`
- **Web App:** Serve locally with `python -m http.server 8080`, then open in your browser at `http://localhost:8080`.

## Acknowledgments & AI Assistance Disclosure

GlitchArchive was designed, architected, and built as an independent systems and data-encoding project. Generative AI tools (Google Gemini) were used for suggesting updates and assisting in the generation of the `README.md` by giving format tricks like ```(language) then end with ``` etc.