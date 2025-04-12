import random

class ChessAI:
    # Chess piece values
    piece_scores = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
    CHECKMATE_SCORE = 1000
    STALEMATE_SCORE = 0
    MAX_DEPTH = 3  # Depth for MinMax algorithm

    # @staticmethod
    # def find_best_move(gs, valid_moves):
    #     turn_indicator = 1 if gs.white_to_move else -1
    #     opponent_min_max_score = ChessAI.CHECKMATE_SCORE

    #     best_player_move = None
    #     random.shuffle(valid_moves)  
    #     for player_move in valid_moves:
    #         gs.make_move(player_move)
    #         opponents_moves = gs.get_valid_moves()

    #         opponent_max_score = -ChessAI.CHECKMATE_SCORE
    #         for opponent_move in opponents_moves:
    #             gs.make_move(opponent_move)
    #             if gs.check_mate:
    #                 score = -turn_indicator * ChessAI.CHECKMATE_SCORE
    #             elif gs.stale_mate:
    #                 score = ChessAI.STALEMATE_SCORE
    #             else:
    #                 score =  -turn_indicator * ChessAI.score_material(gs.board)

    #             if score > opponent_max_score:
    #                 opponent_max_score = score
                
    #             gs.undo_move()
            
    #         # mimimizing opponent's best move
    #         if opponent_max_score < opponent_min_max_score:
    #             opponent_min_max_score = opponent_max_score
    #             best_player_move = player_move
            
    #         gs.undo_move()

    #     return best_player_move
    
    @staticmethod
    def find_best_move_min_max(gs, valid_moves):
        """Helper function to make first recursive call."""
        global next_move
        next_move = None
        ChessAI.find_move_min_max(gs, valid_moves , ChessAI.MAX_DEPTH , gs.white_to_move)
        return next_move

    @staticmethod
    def find_move_min_max(gs, valid_moves, depth, white_to_move):
        global next_move

        if depth == 0:
            return ChessAI.score_material(gs.board)
        
        if white_to_move:
            max_score = -ChessAI.CHECKMATE_SCORE
            for move in valid_moves:
                gs.make_move(move)
                next_valid_moves = gs.get_valid_moves()
                score = ChessAI.find_move_min_max(gs, next_valid_moves, depth - 1, False)

                if score > max_score:
                    max_score = score
                    if depth == ChessAI.MAX_DEPTH:
                        next_move = move        

                gs.undo_move()

            return max_score
        else:
            min_score = ChessAI.CHECKMATE_SCORE
            for move in valid_moves:
                gs.make_move(move)
                next_valid_moves = gs.get_valid_moves()
                score = ChessAI.find_move_min_max(gs, next_valid_moves, depth - 1, True)
                
                if score < min_score:
                    min_score = score
                    if depth == ChessAI.MAX_DEPTH:
                        next_move = move
                
                gs.undo_move()
            
            return min_score
        

    @staticmethod
    def score_board(gs):
        """Score the board for the current player."""
        # positive score better for white, negative for black

        if gs.check_mate:
            if gs.white_to_move:
                return -ChessAI.CHECKMATE_SCORE # black wins
            else:
                return ChessAI.CHECKMATE_SCORE # white wins
            
        elif gs.stale_mate:
            return ChessAI.STALEMATE_SCORE
        

        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == "w":
                    score += ChessAI.piece_scores[square[1]]
                elif square[0] == "b":
                    score -= ChessAI.piece_scores[square[1]]

        return score

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
