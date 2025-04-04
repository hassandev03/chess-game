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

    square_selected = () # keep track of the last square selected (x, y)
    player_clicks = [] # keep track of player clicks; two tuples: [(x1, y1), (x2, y2)]
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # get mouse position (x, y)
                col = location[0] // configs.SQUARE_SIZE
                row = location[1] // configs.SQUARE_SIZE

                if square_selected == (row, col): # user clicked the same square twice
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected) # append for both first and second clicks

                if len(player_clicks) == 2: # after two clicks
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move) # make the move on the board

                    # reset the user clicks and moves
                    square_selected = ()
                    player_clicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()

        clock.tick(configs.MAX_FPS)
        Graphics.draw_game_state(screen, gs)
        p.display.flip()




if __name__ == "__main__":
    main()