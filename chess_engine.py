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
        self.move_functions = {
            "P": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves}
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        """Make a move on the board"""
        self.board[move.start_row][move.start_col] = "--" # remove the piece from the old square
        self.board[move.end_row][move.end_col] = move.piece_moved # move the piece to the new square
        self.move_log.append(move) # log the move
        
        self.white_to_move = not self.white_to_move # switch turns

    def undo_move(self):
        """Undo the last move made"""
        if len(self.move_log) != 0: # check if there are any moves to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_all_possible_moves(self):
        """Get all possible moves for the current player"""
        moves = []
        for row in range(len(self.board)): # rows of the board
            for col in range(len(self.board[row])): #  columns of the board
                turn = self.board[row][col][0] # get the color of the piece
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]

                    # call the appropriate function to get the moves
                    self.move_functions[piece](row, col, moves)

        return moves
        
    def get_valid_moves(self):
        """Get all valid moves for the current player"""
        return self.get_all_possible_moves()
    

    """
    the following methods are used to get the moves for each piece type
    """
    
    def get_pawn_moves(self, row, col, moves):
        """Get all possible moves for a pawn"""

        # white pawn moves
        if self.white_to_move: 
            if self.board[row - 1][col] == "--": # 1 square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--': # 2 square pawn advance
                    moves.append(Move((row, col), (row - 2, col), self.board))

            # capture diagonally
            if col - 1 >= 0: # capture left
                if self.board[row - 1][col - 1][0] == "b": # capture left
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if col + 1 <= 7: # capture right
                if self.board[row - 1][col + 1][0] == "b": # capture right
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        # black pawn moves
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            
            # capture diagonally
            if col - 1 >= 0: # capture left
                if self.board[row + 1][col - 1][0] == "w": # capture left
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            
            if col + 1 <= 7: # capture right
                if self.board[row + 1][col + 1][0] == "w": # capture right
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
        
    
    def get_rook_moves(self, row, col, moves):
        """Get all possible moves for a rook"""

    def get_knight_moves(self, row, col, moves):
        """Get all possible moves for a knight"""

    def get_bishop_moves(self, row, col, moves):
        """Get all possible moves for a bishop"""

    def get_queen_moves(self, row, col, moves):
        """Get all possible moves for a queen"""

    def get_king_moves(self, row, col, moves):
        """Get all possible moves for a king"""
    

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

        self.move_id = self.start_row + self.start_col * 10 + self.end_row * 100 + self.end_col * 1000

    
    def __eq__(self, other):
        """Check if two moves are equal"""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """returns the chess notation of the move"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, row, col):
        """returns the rank and file of the square"""
        return self.cols_to_files[col] + self.rows_to_ranks[row]