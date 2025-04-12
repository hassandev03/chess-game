import pygame as p

WIDTH = HEIGHT = 512  # assuming 512x512 board size based on your code
DIMENSION = 8  # 8x8 chess board
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

# Images dictionary
IMAGES = {}

# Colors
LIGHT_SQUARE = p.Color("white")
DARK_SQUARE = p.Color("burlywood4")
HIGHLIGHT_COLOR = p.Color("yellow")
SELECTED_COLOR = p.Color("blue")
# Game state flags
PROMOTION_ACTIVE = False
PROMOTION_MOVE = None
PROMOTION_CHOICES = ["Q", "R", "B", "N"]  # Queen, Rook, Bishop, Knight

def load_images():
    """Load the chess piece images"""
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
        )