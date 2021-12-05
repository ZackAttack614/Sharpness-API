import requests
import chess
import chess.pgn
import io

PGN = ""
s = requests.Session()
broadcastRoundId = 'JpzVMp2V'

def current_fen(PGN):
    wcc_game = chess.pgn.read_game(PGN)
    board = wcc_game.board()
    for move in wcc_game.mainline_moves():
        board.push(move)
    return board.fen()

with s.get(f'https://lichess.org/api/broadcast/round/{broadcastRoundId}.pgn', stream=True) as resp:
  for line in resp.iter_lines():
    if line:
      if line.startswith(b"1."):
        PGN = io.StringIO(str(line))
        print(current_fen(PGN))
