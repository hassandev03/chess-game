import pygame as p

WIDTH = 512
HEIGHT = 512
DIMENSION = 8 # 8x8 board
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15 # for animations

# global dictionary for images
IMAGES = {}
def load_images():
    pieces = ['bK', 'bN', 'bB', 'bQ', 'bR', 'bP', 'wK', 'wN', 'wB', 'wQ', 'wR', 'wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))