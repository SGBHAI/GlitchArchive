import sys
import math
import base64
from datetime import datetime
import chess
import chess.pgn
from .core import pack_blob, unpack_blob

def encode(file_path, pgn_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
    blob = pack_blob(file_path, raw_data)
    encoded_data = base64.b64encode(blob).decode('utf-8')
    
    current_date = datetime.now().strftime("%Y.%m.%d")
    game = chess.pgn.Game()
    game.headers["Event"] = "GlitchArchive Secure Vault"
    game.headers["Site"] = "GitHub SGBHAI/GlitchArchive"
    game.headers["Date"] = current_date
    game.headers["White"] = "GlitchArchive Encoder"
    game.headers["Black"] = "Chess PGN Carrier"
    game.headers["PayloadData"] = encoded_data
    
    with open(pgn_path, 'w') as f:
        print(game, file=f)

def decode(pgn_path, output_file):
    with open(pgn_path) as f:
        game = chess.pgn.read_game(f)
    
    if not game or "PayloadData" not in game.headers:
        raise ValueError("Invalid PGN: PayloadData header missing")
    
    encoded_data = game.headers["PayloadData"]
    binary_data = base64.b64decode(encoded_data)
    filename, raw, sha = unpack_blob(binary_data)
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])