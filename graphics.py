import pygame as p
import configs

class Graphics:
    @staticmethod
    def draw_game_state(screen, gs):
        """Draw the current state of the game"""
        Graphics.draw_board(screen)  # draw squares on the board
        Graphics.draw_pieces(screen, gs.board)  # draw pieces on top of squares

    @staticmethod
    def draw_board(screen):
        """Draw the squares on the board"""
        colors = [p.Color("white"), p.Color("burlywood4")]
        for r in range(configs.DIMENSION):
            for c in range(configs.DIMENSION):
                color = colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c * configs.SQUARE_SIZE, r * configs.SQUARE_SIZE, 
                                                configs.SQUARE_SIZE, configs.SQUARE_SIZE))

    @staticmethod
    def draw_pieces(screen, board):
        """Draw the pieces on the board using the current game state"""
        for r in range(configs.DIMENSION):
            for c in range(configs.DIMENSION):
                piece = board[r][c]
                if piece != "--":  # not empty square
                    screen.blit(configs.IMAGES[piece], p.Rect(c * configs.SQUARE_SIZE, r * configs.SQUARE_SIZE, 
                                                        configs.SQUARE_SIZE, configs.SQUARE_SIZE))

    @staticmethod
    def draw_promotion_menu(screen, col, promoting_white):
        """Draw the promotion menu"""
        # Background for the promotion menu
        menu_height = 4 * configs.SQUARE_SIZE
        row = 2 if promoting_white else 4  # Position the menu in a reasonable place
        
        # Draw background
        p.draw.rect(screen, p.Color("dark gray"), 
                    p.Rect(col * configs.SQUARE_SIZE, 
                          row * configs.SQUARE_SIZE, 
                          configs.SQUARE_SIZE, menu_height))
        
        # Draw pieces to choose from (Q, R, B, N)
        color_prefix = "w" if promoting_white else "b"
        pieces = ["Q", "R", "B", "N"]
        
        for i, piece in enumerate(pieces):
            piece_key = color_prefix + piece
            screen.blit(configs.IMAGES[piece_key], 
                        p.Rect(col * configs.SQUARE_SIZE, 
                              (row + i) * configs.SQUARE_SIZE, 
                              configs.SQUARE_SIZE, configs.SQUARE_SIZE))

    @staticmethod
    def get_promotion_choice(pos, col, promoting_white):
        """Get the user's promotion choice based on mouse position"""
        x, y = pos
        if x // configs.SQUARE_SIZE == col:
            row = 2 if promoting_white else 4  # Match the starting row in draw_promotion_menu
            selected_row = y // configs.SQUARE_SIZE
            
            if row <= selected_row < row + 4:
                index = selected_row - row
                return configs.PROMOTION_CHOICES[index]
        
        return None  # No valid selection
