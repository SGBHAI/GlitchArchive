import sys
import math
import chess
import chess.pgn
from core import pack_blob, unpack_blob

def encode(file_path, pgn_path):
    blob = pack_blob(file_path)
    bits = "".join(f"{b:08b}" for b in blob)
    board = chess.Board()
    game = chess.pgn.Game()
    node = game
    bit_idx = 0
    while bit_idx < len(bits) and not board.is_game_over():
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            break
        num_moves = len(legal_moves)
        bits_per_move = math.floor(math.log2(num_moves))
        if bits_per_move < 1:
            move = legal_moves[0]
            node = node.add_variation(move)
            board.push(move)
            continue
        chunk = bits[bit_idx:bit_idx + bits_per_move]
        if len(chunk) < bits_per_move:
            chunk = chunk.ljust(bits_per_move, '0')
        move_idx = int(chunk, 2) % num_moves
        bit_idx += bits_per_move
        move = legal_moves[move_idx]
        node = node.add_variation(move)
        board.push(move)
    game.headers["Event"] = "GlitchArchive Chess Vault"
    game.headers["Site"] = "GitHub SGBHAI/GlitchArchive"
    game.headers["Date"] = "2026.11.08"
    game.headers["White"] = "GlitchArchive Encoder"
    game.headers["Black"] = "Chess PGN Carrier"
    with open(pgn_path, 'w') as f:
        print(game, file=f)

def decode(pgn_path, output_file):
    with open(pgn_path) as f:
        game = chess.pgn.read_game(f)
    board = game.board()
    node = game
    bit_strings = []
    while node.variations:
        next_node = node.variation(0)
        move = next_node.move
        legal_moves = list(board.legal_moves)
        num_moves = len(legal_moves)
        bits_per_move = math.floor(math.log2(num_moves))
        if bits_per_move >= 1:
            move_idx = legal_moves.index(move)
            chunk = bin(move_idx)[2:].zfill(bits_per_move)
            bit_strings.append(chunk)
        board.push(move)
        node = next_node
    all_bits = "".join(bit_strings)
    byte_array = bytearray()
    for i in range(0, len(all_bits) - 7, 8):
        byte_array.append(int(all_bits[i:i+8], 2))
    _, raw = unpack_blob(bytes(byte_array))
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])