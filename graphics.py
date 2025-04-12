import pygame as p
import configs

class Graphics:
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
    def highlight_squares(screen, gs, valid_moves, selected_square):
        """Highlight the squares on the board"""
        if selected_square != ():
            row, col = selected_square
            # selected square is a piece that can be moved
            if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
                surface = p.Surface((configs.SQUARE_SIZE, configs.SQUARE_SIZE))
                surface.set_alpha(100)
                surface.fill(p.Color(configs.SELECTED_COLOR))
                screen.blit(surface, (col * configs.SQUARE_SIZE, row * configs.SQUARE_SIZE))

                # highlight valid moves
                surface.fill(p.Color(configs.HIGHLIGHT_COLOR))
                for move in valid_moves:
                    if move.start_row == row and move.start_col == col:
                        screen.blit(surface, (move.end_col * configs.SQUARE_SIZE, move.end_row * configs.SQUARE_SIZE))

    @staticmethod
    def draw_game_state(screen, gs, valid_moves, selected_square):
        """Draw the current state of the game"""
        Graphics.draw_board(screen)  # draw squares on the board
        Graphics.highlight_squares(screen, gs, valid_moves, selected_square)
        Graphics.draw_pieces(screen, gs.board)  # draw pieces on top of squares
        
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
    
    @staticmethod
    def animate_move(move, screen, board, clock):
        colors = [p.Color("white"), p.Color("burlywood4")]
        dRow = move.end_row - move.start_row
        dCow = move.end_col - move.start_col

        frames_per_square = 10  # frames to move one square
        frame_count = (abs(dRow) + abs(dCow)) * frames_per_square  # total frames to animate

        # Get the piece being moved
        for frame in range(frame_count + 1): # + 1 to include the end position
            row, col = (move.start_row + dRow * frame // frame_count, move.start_col + dCow * frame // frame_count)
            
            Graphics.draw_board(screen)
            Graphics.draw_pieces(screen, board)

            # erase the piece from the starting square
            color = colors[(move.end_row + move.end_col) % 2]
            end_square = p.Rect(move.end_col * configs.SQUARE_SIZE, move.end_row * configs.SQUARE_SIZE, 
                                configs.SQUARE_SIZE, configs.SQUARE_SIZE)
            p.draw.rect(screen, color, end_square)

            # draw the captured piece onto the rectangl if any
            if move.piece_captured != "--":
                screen.blit(configs.IMAGES[move.piece_captured], end_square)

            # draw the moving piece
            screen.blit(configs.IMAGES[move.piece_moved], 
                        p.Rect(col * configs.SQUARE_SIZE, row * configs.SQUARE_SIZE, 
                               configs.SQUARE_SIZE, configs.SQUARE_SIZE))
            
            p.display.flip()
            clock.tick(60)  

    @staticmethod
    def display_text(screen, text):
        """Display text on the screen"""
        font = p.font.SysFont("Roboto", 50, False, True)
        text_object = font.render(text, True, p.Color("gray"))
        text_location = p.Rect(0, 0, configs.WIDTH, configs.HEIGHT).move(configs.WIDTH // 2 - text_object.get_width() // 2, 
                                   configs.HEIGHT // 2 - text_object.get_height() // 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, True, p.Color("cyan"))
        screen.blit(text_object, text_location.move(1, -2))  # Slightly offset for shadow effect
        
