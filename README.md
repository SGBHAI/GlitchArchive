# GlitchArchive 🚀

A multi-carrier lossless "weird storage" vault engineered to store arbitrary files inside unconventional digital media—including RGB Pixel Matrices, Pixel Streams, and Chess PGN Containers—with bit-perfect SHA-256 validation.

Built as an advanced systems and data-encoding project for the Hack Club card.

## Architecture & Binary Specification

GlitchArchive uses a unified binary serialization format wrapped in custom carrier containers. Every archive is packaged using the `core.py` serialization engine.

### The `WSTR` Header Layout

Every encoded payload begins with a standardized 11-byte header followed by the DEFLATE-compressed payload:

| Offset  | Size     | Type              | Description                             | 
| -----   | -----    | -----             | -----                                   | 
| `0 - 3` | 4 bytes  | ASCII / Byte Array| Magic bytes: `[87, 83, 84, 82]` (`WSTR`)| 
| `4`     | 1 byte   | Unsigned Byte     | File name length (`N`)                  | 
| `5 - 8` | 4 bytes  | Big-Endian Uint32 | Compressed payload length               | 
| `9 - 10`| 2 bytes  | Unsigned Uint16   | Raw uncompressed file size              | 
| `11`    | `N` bytes| UTF-8 String      | Original filename                       | 
| `11 + N`| Variable | Byte Stream       | DEFLATE-compressed binary payload       | 

## Carrier Modules

GlitchArchive implements robust, fully functioning storage carriers:

1. **Lossless RGB Pixel Matrix (`glitch_image.py` / Web)**: Packs serialized blobs directly into square-proportioned RGB pixel channels of uncompressed PNG images. Best for compact storage.

2. **Lossless Pixel Matrix Stream (`glitch_video.py` / Web)**: Packs serialized blobs into a fixed 320px wide row stride. Best for streaming and frame-interleaved simulation.

3. **Chess PGN (`glitch_chess.py` / Web)**: Encodes arbitrary binary data into custom metadata headers (`[PayloadData]`) of PGN chess game notation files. Best for social sharing.

## Requirements & Dependencies

Install all necessary dependencies for the Python CLI modules using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Local Development & Installation

### Prerequisites

* Python 3.10+
* Required Python libraries (listed in `requirements.txt`)

### Installation & Setup

```bash
git clone https://github.com/SGBHAI/GlitchArchive.git
cd glitcharchive
pip install -r requirements.txt
```

### Usage (CLI Test Suite)

#### Encode Payload to Carrier:

```powershell
python src/glitch_video.py enc test_input.txt test_archive.avi
```

#### Decode Carrier to Recover Payload:

```powershell
python src/glitch_video.py dec test_archive.avi test_recovered_video.txt
```

#### Verify Data Integrity (SHA-256 Hash Validation):

```powershell
Get-FileHash test_input.txt, test_recovered_video.txt -Algorithm SHA256
```

## Web Interface & Live Deployment

GlitchArchive features a fully client-side browser dashboard (`index.html`) utilizing the HTML5 Canvas API and Web Streams API (`CompressionStream` / `DecompressionStream`) for zero-setup, lightning-fast in-browser encoding and decoding.

* **Live Preview / Production URL**: https://sgbhai.github.io/GlitchArchive/
* **Hosting**: Automatically deployed and hosted via GitHub Pages directly from the main branch.

## Acknowledgments & AI Assistance Disclosure

GlitchArchive was designed, architected, and built as an independent systems and data-encoding project. Generative AI tools (Google Gemini) were used for suggesting updates and generating the `README.md`.