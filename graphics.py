"""
draws the graphics of the game with the current game state
"""
import pygame as p
import configs

class Graphics:
    """
    Responsible for graphics and displaying the game state
    """
    def draw_board(screen):
        """ draws the squares on the board"""
        colors = [p.Color("white"), p.Color("gray")]
        for row in range(configs.DIMENSION):
            for col in range(configs.DIMENSION):
                color = colors[((row + col) % 2)]
                p.draw.rect(screen, color, p.Rect(col * configs.SQUARE_SIZE, row * configs.SQUARE_SIZE, configs.SQUARE_SIZE, configs.SQUARE_SIZE))


    
    def draw_pieces(screen, board):
        """
        draws the pieces on the board
        """
        for row in range(configs.DIMENSION):
            for col in range(configs.DIMENSION):
                piece = board[row][col]
                if piece != "--": # not an empty square
                    screen.blit(configs.IMAGES[piece], p.Rect(col * configs.SQUARE_SIZE, row * configs.SQUARE_SIZE, configs.SQUARE_SIZE, configs.SQUARE_SIZE))

    def draw_game_state(screen, gs):
        Graphics.draw_board(screen) # draw squares on the board
        Graphics.draw_pieces(screen, gs.board) # draw pieces on top of those squares

    

    