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
    p.init()  # initialize pygame
    p.display.set_caption("Chess")
    screen = p.display.set_mode((configs.WIDTH, configs.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()

    valid_moves = gs.get_valid_moves()  # get all valid moves for the current player
    move_made = False  # flag to check if a move was made
    
    # New promotion handling variables
    promotion_active = False
    promotion_move = None

    configs.load_images()  # load images once

    square_selected = ()  # keep track of the last square selected (row, col)
    player_clicks = []  # keep track of player clicks; two tuples: [(row1, col1), (row2, col2)]
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:
                if not promotion_active:
                    location = p.mouse.get_pos()  # get mouse position (x, y)
                    col = location[0] // configs.SQUARE_SIZE
                    row = location[1] // configs.SQUARE_SIZE

                    if square_selected == (row, col):  # user clicked the same square twice
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both first and second clicks

                    if len(player_clicks) == 2:  # after two clicks
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())

                        # Check if the move is in valid moves
                        valid_move = None
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                valid_move = valid_moves[i]
                                break
                                
                        if valid_move:
                            # If the move is a pawn promotion
                            if valid_move.is_pawn_promotion:
                                promotion_active = True
                                promotion_move = valid_move
                                # Reset clicks but don't make the move yet
                                square_selected = ()
                                player_clicks = []
                            else:
                                # Make a normal move
                                gs.make_move(valid_move)
                                move_made = True
                                square_selected = ()
                                player_clicks = []
                        else:
                            player_clicks = [square_selected]
                    
                else:  # Promotion is active, handle piece selection
                    location = p.mouse.get_pos()
                    promotion_choice = Graphics.get_promotion_choice(
                        location, 
                        promotion_move.end_col, 
                        promotion_move.piece_moved[0] == "w"
                    )
                    
                    if promotion_choice:
                        # Create a new move with the promotion choice
                        new_promotion_move = chess_engine.Move(
                            (promotion_move.start_row, promotion_move.start_col),
                            (promotion_move.end_row, promotion_move.end_col),
                            gs.board,
                            promotion_choice=promotion_choice
                        )
                        gs.make_move(new_promotion_move)
                        move_made = True
                        promotion_active = False
                        promotion_move = None

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo the last move made
                    gs.undo_move()
                    move_made = True
                    promotion_active = False  # Cancel any active promotion
                    promotion_move = None

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        Graphics.draw_game_state(screen, gs)
        
        # Draw promotion menu if active
        if promotion_active:
            Graphics.draw_promotion_menu(
                screen, 
                promotion_move.end_col,
                promotion_move.piece_moved[0] == "w"
            )
        
        p.display.flip()
        clock.tick(configs.MAX_FPS)

if __name__ == "__main__":
    main()