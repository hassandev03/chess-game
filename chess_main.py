"""
this is responsible for handling user input and running the whole game and
displaying current GameState object
"""
import pygame as p
import chess_engine
from graphics import Graphics
import configs


# main game driver
def main():
    p.init() # initialize pygame
    p.display.set_caption("Chess")
    screen = p.display.set_mode((configs.WIDTH, configs.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    print(gs.board)
    configs.load_images() # load images once

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(configs.MAX_FPS)
        Graphics.draw_game_state(screen, gs)
        p.display.flip()




if __name__ == "__main__":
    main()