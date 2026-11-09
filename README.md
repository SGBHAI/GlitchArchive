# GlitchArchive 🚀

A multi-carrier lossless "weird storage" vault engineered to store arbitrary files inside unconventional digital media—including PNG pixel matrices, XLSX spreadsheets, WAV audio modem frequency streams, PGN chess games, and raw lossless video streams—with bit-perfect SHA-256 validation.

Built as an advanced systems and data-encoding project for the Hack Club card.

---

## Architecture & Binary Specification

GlitchArchive uses a unified binary serialization format wrapped in custom carrier containers. Every archive is packaged using the `core.py` serialization engine.

### The `WSTR` Header Layout
Every encoded payload begins with a standardized 11-byte header followed by the DEFLATE-compressed payload:

| Offset  | Size     | Type               | Description                              | 
| :---    | :---     | :--- | :---        |                :---------                |
| `0 - 3` | 4 bytes  | ASCII / Byte Array | Magic bytes: `[87, 83, 84, 82]` (`WSTR`) |
| `4`     | 1 byte   | Unsigned Byte      | File name length (`N`)                   | 
| `5 - 8` | 4 bytes  | Big-Endian Uint32  | Compressed payload length                |
| `9 - 10`| 2 bytes  | Unsigned Uint16    | Raw uncompressed file size               |  
| `11`    | `N` bytes| UTF-8 String       | Original filename                        |
| `11 + N`| Variable | Byte Stream        | DEFLATE-compressed binary payload        |

---

## Carrier Modules

GlitchArchive implements five distinct storage carriers:

1. **Lossless Image Matrix (`glitch_image.py`)**: Packs serialized blobs directly into RGB pixel channels of uncompressed PNG images, utilizing automatic dimension scaling to prevent data loss.
2. **Spreadsheet Grid (`glitch_spreadsheet.py`)**: Maps binary chunks into RGB cell color values within `.xlsx` spreadsheet grids.
3. **Audio Modem (`glitch_audio.py`)**: Converts binary streams into frequency-modulated audio frequency shift keying (FSK) WAV modem tones.
4. **Chess PGN (`glitch_chess.py`)**: Encodes arbitrary data into valid move sequences and metadata fields of PGN chess game notation files.
5. **Lossless Video Stream (`glitch_video.py`)**: Interleaves binary payloads across uncompressed frame buffers using lossless codecs (`HFYU`) to bypass chroma subsampling and inter-frame compression artifacts.

---

## Local Development & CLI Usage

### Prerequisites
* Python 3.10+
* OpenCV (`cv2`), NumPy, Pillow, Openpyxl

### Installation & CLI Execution Commands

```powershell
# Clone the repository
git clone https://github.com/SGBHAI/GlitchArchive.git
cd glitcharchive

# Install dependencies
pip install -r requirements.txt

# Encode payload to video carrier
python src/glitch_video.py enc test_input.txt test_archive.avi

# Decode carrier to recover payload
python src/glitch_video.py dec test_archive.avi test_recovered_video.txt

# Verify data integrity (SHA-256 hash validation)
Get-FileHash test_input.txt, test_recovered_video.txt -Algorithm SHA256
```

---

## Web Interface & Live Deployment

GlitchArchive features a fully client-side browser dashboard (`index.html`) utilizing the HTML5 Canvas API and Web Streams API (`CompressionStream` / `DecompressionStream`) for zero-setup, lightning-fast in-browser encoding and decoding.

* **Live Web Vault**: [https://sgbhai.github.io/GlitchArchive/](https://sgbhai.github.io/GlitchArchive/)
* **Hosting**: Automated continuous deployment via GitHub Pages on the `main` branch.