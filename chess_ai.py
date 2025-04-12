import random

class ChessAI:
    # Chess piece values
    piece_scores = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
    CHECKMATE_SCORE = 1000
    STALEMATE_SCORE = 0

    @staticmethod
    def find_best_move(gs, valid_moves):
        turn_indicator = 1 if gs.white_to_move else -1
        opponent_min_max_score = ChessAI.CHECKMATE_SCORE

        best_player_move = None
        random.shuffle(valid_moves)  
        for player_move in valid_moves:
            gs.make_move(player_move)
            opponents_moves = gs.get_valid_moves()

            opponent_max_score = -ChessAI.CHECKMATE_SCORE
            for opponent_move in opponents_moves:
                gs.make_move(opponent_move)
                if gs.check_mate:
                    score = -turn_indicator * ChessAI.CHECKMATE_SCORE
                elif gs.stale_mate:
                    score = ChessAI.STALEMATE_SCORE
                else:
                    score =  -turn_indicator * ChessAI.score_material(gs.board)

                if score > opponent_max_score:
                    opponent_max_score = score
                
                gs.undo_move()
            
            # mimimizing opponent's best move
            if opponent_max_score < opponent_min_max_score:
                opponent_min_max_score = opponent_max_score
                best_player_move = player_move
            
            gs.undo_move()

        return best_player_move

    @staticmethod
    def score_material(board):
        """Calculate the material score of the board."""
        score = 0
        for row in board:
            for square in row:
                if square[0] == "w":
                    score += ChessAI.piece_scores[square[1]]
                elif square[0] == "b":
                    score -= ChessAI.piece_scores[square[1]]

        return score
        return score
