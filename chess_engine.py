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
        #   P -> Pawn, R -> Rook, B -> Bishop, Q -> Queen, K -> King, N -> Knight
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

        self.white_king_location = (7, 4) # row, col
        self.black_king_location = (0, 4) # row, col

        self.check_mate = False
        self.stale_mate = False

        self.en_passant_possible = ()

    def make_move(self, move):
        """Make a move on the board"""
        self.board[move.start_row][move.start_col] = "--"  # remove the piece from the old square
        self.board[move.end_row][move.end_col] = move.piece_moved  # move the piece to the new square
        self.move_log.append(move)  # log the move
        
        # update the king's location if the piece moved is a king
        if move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)

        # check if the move is a pawn promotion
        if move.is_pawn_promotion:
            if move.promotion_choice:
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + move.promotion_choice
            else:
                # Default to Queen if no choice provided (for simplicity)
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        # en-passant move
        if move.is_en_passant_move:
            if move.piece_moved[0] == "w":  # White pawn capturing black pawn
                self.board[move.start_row][move.end_col] = "--"  # remove the captured black pawn
            else:  # Black pawn capturing white pawn
                self.board[move.start_row][move.end_col] = "--"  # remove the captured white pawn

        # update en-passant possible variable
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:  # pawn moved two squares
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)  # set the en-passant square
        else:
            self.en_passant_possible = ()

        # After making the move, switch turns only if this wasn't a promotion without a choice
        if not (move.is_pawn_promotion and not move.promotion_choice):
            self.white_to_move = not self.white_to_move  # switch turns

    def undo_move(self):
        """Undo the last move made"""
        if len(self.move_log) != 0: # check if there are any moves to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            # undo the king's location 
            if move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)

            # undo en passant 
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = "--" # leaving landing square blank
                if move.piece_moved[0] == "w":  # White was capturing black pawn
                    self.board[move.start_row][move.end_col] = "bP" # restore the captured black pawn
                else:  # Black was capturing white pawn
                    self.board[move.start_row][move.end_col] = "wP" # restore the captured white pawn
                self.en_passant_possible = (move.end_row, move.end_col)

            # undo two square pawn advance
            if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()
            
            self.white_to_move = not self.white_to_move

            self.check_mate = False
            self.stale_mate = False

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

        temp_en_passant_possible = self.en_passant_possible # store the current en-passant variable
        # first get all possible moves
        moves = self.get_all_possible_moves()
        # for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            # when make_move is called, the turn is switched, so we need to change it back to the current player before checking for check
            self.white_to_move = not self.white_to_move

            # generate all possible moves for the opponent and for each move, check if the king is in check
            if self.in_check():
                moves.remove(moves[i])

            self.white_to_move = not self.white_to_move # switch back to the current player's turn
            self.undo_move() # undo the move made to check for check

        # if there are no valid moves, check for checkmate or stalemate
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        self.en_passant_possible = temp_en_passant_possible # reset the en-passant variable
        return moves # return the valid moves

    def in_check(self):
        """Check if the current player is in check"""
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])


    def square_under_attack(self, row, col):
        """Check if a square is under attack by enemy"""
        self.white_to_move = not self.white_to_move # switch to opponent's turn
        enemy_moves = self.get_all_possible_moves() # get all possible moves for the opponent
        self.white_to_move = not self.white_to_move # switch back to current player's turn

        for move in enemy_moves:
            if move.end_row == row and move.end_col == col: # check if the move ends on the square
                return True # square is under attack

        return False # square is not under attack


    """
    the following methods are used to get the moves for each piece type
    """

    def get_pawn_moves(self, row, col, moves):
        """Get all possible moves for a pawn"""

        # white pawn moves
        if self.white_to_move:
            if row > 0 and self.board[row - 1][col] == "--": # 1 square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--': # 2 square pawn advance
                    moves.append(Move((row, col), (row - 2, col), self.board))

            # capture diagonally
            if col - 1 >= 0 and row > 0: # capture left
                if self.board[row - 1][col - 1][0] == "b": # capture left
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_en_passant_move=True)) # en passant left

            if col + 1 <= 7 and row > 0: # capture right
                if self.board[row - 1][col + 1][0] == "b": # capture right
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_en_passant_move=True)) # en passant right

        # black pawn moves
        else:
            if row < 7 and self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))

            # capture diagonally
            if col - 1 >= 0 and row < 7: # capture left
                if self.board[row + 1][col - 1][0] == "w": # capture left
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_en_passant_move=True)) # en passant left

            if col + 1 <= 7 and row < 7: # capture right
                if self.board[row + 1][col + 1][0] == "w": # capture right
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_en_passant_move=True)) # en passant right


    def get_rook_moves(self, row, col, moves):
        """Get all possible moves for a rook"""
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # up, down, right, left
        enemy_color = "b" if self.white_to_move else "w"

        for dir in directions:
            for i in range(1, 8): # can move at max 7 squares in 4 basic directions
                # calculate the new row and column
                new_row = row + dir[0] * i
                new_col = col + dir[1] * i
                if 0 <= new_row < 8 and 0 <= new_col < 8: # check if the new square is on the board

                    end_piece = self.board[new_row][new_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (new_row, new_col), self.board))

                    elif end_piece[0] == enemy_color: # capture the piece
                        moves.append(Move((row, col), (new_row, new_col), self.board))
                        break # stop moving in this direction

                    else: # friendly piece
                        break # stop moving in this direction
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        """Get all possible moves for a knight"""
        knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]  # all possible knight moves
        ally_color = "w" if self.white_to_move else "b"

        for move in knight_moves:
            new_row = row + move[0]
            new_col = col + move[1]

            # knight can jump over pieces, so we don't need to check for empty squares in between
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                end_piece = self.board[new_row][new_col]
                if end_piece[0] != ally_color: # not a friendly piece; either empty or enemy piece
                    moves.append(Move((row, col), (new_row, new_col), self.board))


    def get_bishop_moves(self, row, col, moves):
        """Get all possible moves for a bishop"""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # up-left, up-right, down-left, down-right
        enemy_color = "b" if self.white_to_move else "w"

        for dir in directions:
            for i in range(1, 8): # can move at max 7 squares diagonally
                # calculate the new row and column
                new_row = row + dir[0] * i
                new_col = col + dir[1] * i
                if 0 <= new_row < 8 and 0 <= new_col < 8: # check if the new square is on the board

                    end_piece = self.board[new_row][new_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (new_row, new_col), self.board))

                    elif end_piece[0] == enemy_color: # capture the piece
                        moves.append(Move((row, col), (new_row, new_col), self.board))
                        break # stop moving in this direction

                    else: # friendly piece
                        break # stop moving in this direction
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        """Get all possible moves for a queen"""
        # queen moves like a rook and bishop combined
        # so we can just call the rook and bishop move functions
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """Get all possible moves for a king"""
        # king can move one square in any direction, so we can just check all 8 possible moves
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        ally_color = "w" if self.white_to_move else "b"

        for i in range(len(king_moves)):
            new_row = row + king_moves[i][0]
            new_col = col + king_moves[i][1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                    end_piece = self.board[new_row][new_col]
                    if end_piece[0] != ally_color: # not a friendly piece; either empty or enemy piece
                        moves.append(Move((row, col), (new_row, new_col), self.board))


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

    def __init__(self, start_square, end_square, board, is_en_passant_move=False, promotion_choice=None):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        self.move_id = self.start_row + self.start_col * 10 + self.end_row * 100 + self.end_col * 1000

        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7)
        self.promotion_choice = promotion_choice

        # en passant
        self.is_en_passant_move = is_en_passant_move
        if self.is_en_passant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"


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