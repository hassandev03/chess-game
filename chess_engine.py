"""
it is repsonsible for the chess engine logic and storing the current state
of the game
also determines the valid moves
"""

class GameState:
    """Class to store the current state of the game"""
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

    def make_move(self, move):
        """Make a move on the board"""
        self.board[move.start_row][move.start_col] = "--" # remove the piece from the old square
        self.board[move.end_row][move.end_col] = move.piece_moved # move the piece to the new square
        self.move_log.append(move) # log the move
        
        self.white_to_move = not self.white_to_move # switch turns

    

class Move:
    """Class to store a move made by a player"""

    # using rank and file notation for the chess board
    # ranks are called rows -> 1-8 (1 is the first row, 8 is the last row)
    # files are called columns -> a-h (a is the first column, h is the last column)

    # maps are used to convert between rank/file and row/column
    ranks_to_rows = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0
    }
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]


    def get_chess_notation(self):
        """returns the chess notation of the move"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, row, col):
        """returns the rank and file of the square"""
        return self.cols_to_files[col] + self.rows_to_ranks[row]