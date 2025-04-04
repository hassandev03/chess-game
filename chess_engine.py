"""
it is repsonsible for the chess engine logic and storing the current state
of the game
also determines the valid moves
"""

class GameState:
    def __init__(self):
        # each list represents a row on the board
        # first character represents the color: w -> white, b -> black
        # second character represents the piece:
        #  P -> Pawn, R -> Rook, B -> Bishop, Q -> Queen, K -> King, N -> Knight
        # -- represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.white_to_move = True
        self.move_log = []