# GlitchArchive 🚀

Hey! Welcome to GlitchArchive. This is a weird storage vault I built to hide arbitrary files inside weird carriers—like RGB pixel grids, pixel streams, and even chess PGN game notation files—while keeping everything safe with strict SHA-256 validation. It handles files up to 4 GB.

## What It Is
Basically, GlitchArchive takes any file you throw at it and smashes it into visual or structured formats (like a random PNG image or a chess game text file). You can encode it using my Python scripts or right inside your browser, and then decode it back losslessly. 

## How I Built It
- **Core Engine (`core.py`)**: Handles packaging and unpacking data using zlib compression and a 45-byte header that tracks magic bytes (`WSTR`), file name length, compression metrics, raw lengths, and the 32-bit SHA-256 hash.
- **Carriers**: Made multi-format encoders/decoders for pixel streams, RGB pixel matrices (handling annoying browser RGBA canvas artifacts with `.convert('RGB')`), and chess PGN files using Base64 `PayloadData` headers.
- **Web Interface (`index.html`)**: A frontend built with JavaScript `DataView` and browser canvas APIs so you can pack and unpack files straight from your browser.

## What Was Hard
- **Header Syncing**: Getting the 45-byte header to match precisely between Python's `struct` and JavaScript's `DataView` byte offsets was a massive pain, but necessary so the CLI and web app don't desync.
- **Browser RGBA Fixes**: Browser canvases love saving images in RGBA, which completely broke my CLI decoder's magic byte checks. Had to force `.convert('RGB')` everywhere in Python to fix it.

## Header Table (45 Bytes Base Header + Variable Fields)
| Field       | Size (Bytes) | Type / Description                |
| :---        | :---         | :------------------               |
| `MAGIC`     | 4            | Magic bytes (`WSTR`)              |
| `name_len`  | 1            | Length of original filename (`>B`)|
| `comp_len`  | 4            | Compressed payload length (`>I`)  |
| `raw_len`   | 4            | Uncompressed payload length (`>I`)|
| `SHA-256`   | 32           | Cryptographic hash of raw payload |
| `filename`  | Variable     | UTF-8 encoded original filename   |
| `compressed`| Variable     | DEFLATE compressed binary data    |

## My Experience and reason for picking this card
When I first learned about steganography, I was in total disbelief. It made me wonder how, why, and what it was. So I watched some YouTube videos to figure out how it works, and it actually became one of my 31st projects (though that version was just a bare skeleton and none of that code is here today!). Later, I saw Hack Club on Instagram and joined a space-related hackathon or program, though I honestly can't remember its name. As soon as I joined, it ended. While searching for another program, I found Crescent and saw this card, which instantly reminded me that I had done something similar before. That's why I picked it.

## How to Run
- **Python CLI Pack:** `python -m src.core pack <filename>`
- **Python CLI Unpack:** `python -m src.core unpack <carrier>`
- **Web App:** Run `python -m http.server 8080` and head to `http://localhost:8080` in your browser.

## Acknowledgments & AI Assistance Disclosure

I designed and coded this whole project myself. However, I did use Google Gemini as an AI assistant to help format and rewrite parts of this `README.md` file (like structuring markdown tables and handling code block formatting tricks).