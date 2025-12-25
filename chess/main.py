import pygame
import sys

from constants import *
from game import Game
from square import Square
from move import Move
from button import Button
from engine import Engine

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.start_pieces = "white"
        self.timer = 0
        self.eval_bar = False
        self.winner = ""
        self.g_mode = ""
        # Cache fonts and images
        self._cache_resources()
    
    def _cache_resources(self):
        """Cache fonts and images to avoid reloading every frame"""
        # Cache fonts
        self.font_40 = pygame.font.Font("font.ttf", 40)
        self.font_20 = pygame.font.Font("font.ttf", 20)
        self.font_18 = pygame.font.Font("font.ttf", 18)
        self.font_14 = pygame.font.Font("font.ttf", 14)
        self.font_12 = pygame.font.Font("font.ttf", 12)
        self.font_10 = pygame.font.Font("font.ttf", 10)
        self.font_25 = pygame.font.Font("font.ttf", 25)
        self.font_30 = pygame.font.Font("font.ttf", 30)
        
        # Cache images
        self.bg_image = pygame.transform.scale(pygame.image.load("images/background.png"), (500, 500))
        self.rectangle_img = pygame.image.load("images/rectangle.png")
        self.big_img = pygame.image.load("images/big.png")
        self.small_img = pygame.image.load("images/small.png")
        self.black_img = pygame.image.load("images/black.png")
    
    def main_menu(self):
        screen = self.screen
        pygame.display.set_caption("Menu")
        while True:
            screen.blit(self.bg_image, (0,0))
            mouse_pos = pygame.mouse.get_pos()
            menu_text = self.font_40.render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(250,100))
            rect = (65, 70, 370, 60)
            pygame.draw.rect(screen, pygame.Color("white"), rect)
            screen.blit(menu_text, menu_rect)
            play_button = Button(image=self.rectangle_img, pos=(250, 200), 
                            text_input="PLAY", font=self.font_40, base_colour="black", hovering_colour="White")
            quit_button = Button(image=self.rectangle_img, pos=(250, 275), 
                            text_input="QUIT", font=self.font_40, base_colour="black", hovering_colour="White")

            for button in [play_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(screen)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.game_mode()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    def game_mode(self):
        screen = self.screen
        pygame.display.set_caption("Game Mode")
        player = Button(image=self.big_img, pos=(250, 150), 
                            text_input="2-PLAYER", font=self.font_20, base_colour="black", hovering_colour="White")
        computer = Button(image=self.big_img, pos=(250, 225), 
                            text_input="COMPUTER", font=self.font_20, base_colour="black", hovering_colour="White")
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill("white")
            game_text = self.font_40.render("GAME MODE", True, "#b68f40")
            game_rect = game_text.get_rect(center=(250,35))
            rect = (65, 5, 370, 60)
            pygame.draw.rect(screen, pygame.Color("black"), rect)
            screen.blit(game_text, game_rect)

            buttons = [player, computer]
            for x in buttons:
                x.changeColor(mouse_pos)
                x.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player.checkForInput(mouse_pos):
                        self.g_mode = "2"
                        self.mainloop()
                        
                    elif computer.checkForInput(mouse_pos):
                        self.g_mode = "computer"
                        self.play_menu()

                    

            pygame.display.update()




    def play_menu(self):
        screen = self.screen
        pygame.display.set_caption("Play Menu")
        white = Button(image=self.small_img, pos=(180, 175), 
                            text_input="WHITE", font=self.font_12, base_colour="black", hovering_colour="White")
        black = Button(image=self.small_img, pos=(320, 175), 
                            text_input="BLACK", font=self.font_12, base_colour="black", hovering_colour="White")
        no_t = Button(image=self.small_img, pos=(63, 265), 
                            text_input="NO TIMER", font=self.font_10, base_colour="black", hovering_colour="White")
        min_1 = Button(image=self.small_img, pos=(188, 265), 
                            text_input="1 MINUTE", font=self.font_10, base_colour="black", hovering_colour="White")
        min_5 = Button(image=self.small_img, pos=(312, 265), 
                            text_input="5 MINUTE", font=self.font_10, base_colour="black", hovering_colour="White")
        min_10 = Button(image=self.small_img, pos=(437, 265), 
                            text_input="10 MINUTE", font=self.font_10, base_colour="black", hovering_colour="White")
        on = Button(image=self.small_img, pos=(180, 355), 
                            text_input="ON", font=self.font_12, base_colour="black", hovering_colour="White")
        off = Button(image=self.small_img, pos=(320, 355), 
                            text_input="OFF", font=self.font_12, base_colour="black", hovering_colour="White")
        confirm = Button(image=self.black_img, pos=(250, 460), 
                            text_input="PLAY", font=self.font_25, base_colour="red", hovering_colour="white")
        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill("white")
            options_text = self.font_40.render("OPTIONS", True, "#b68f40")
            options_rect = options_text.get_rect(center=(250,35))
            rect = (65, 5, 370, 60)
            pygame.draw.rect(screen, pygame.Color("black"), rect)
            screen.blit(options_text, options_rect)
            pieces = self.font_18.render("PIECES", True, pygame.Color("white"))
            pieces_rect = pieces.get_rect(center = (250,130))
            rect_2 = self.big_img.get_rect(center = (250,130))
            screen.blit(self.big_img, rect_2)
            screen.blit(pieces, pieces_rect)
            timer = self.font_18.render("TIMER", True, pygame.Color("white"))
            timer_rect = timer.get_rect(center = (250,220))
            rect_3 = self.big_img.get_rect(center = (250,220))
            screen.blit(self.big_img, rect_3)
            screen.blit(timer, timer_rect)
            eval = self.font_14.render("EVALUATION BAR", True, pygame.Color("white"))
            eval_rect = eval.get_rect(center = (250,310))
            rect_4 = self.big_img.get_rect(center = (250,310))
            screen.blit(self.big_img, rect_4)
            screen.blit(eval, eval_rect)
            buttons = [white, black, no_t, min_1, min_5, min_10, on, off, confirm]
            for x in buttons:
                x.changeColor(mouse_pos)
                x.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if white.checkForInput(mouse_pos):
                        self.start_pieces = "white"
                        white.base_colour = "blue"
                        black.base_colour = "black"
                    elif black.checkForInput(mouse_pos):
                        self.start_pieces = "black"
                        black.base_colour = "blue"
                        white.base_colour = "black"
                    if no_t.checkForInput(mouse_pos):
                        self.timer = 0
                        no_t.base_colour = "blue"
                        min_1.base_colour = "black"
                        min_5.base_colour = "black"
                        min_10.base_colour = "black"
                    elif min_1.checkForInput(mouse_pos):
                        self.timer = 1
                        no_t.base_colour = "black"
                        min_1.base_colour = "blue"
                        min_5.base_colour = "black"
                        min_10.base_colour = "black"
                    elif min_5.checkForInput(mouse_pos):
                        self.timer = 5
                        no_t.base_colour = "black"
                        min_1.base_colour = "black"
                        min_5.base_colour = "blue"
                        min_10.base_colour = "black"
                    elif min_10.checkForInput(mouse_pos):
                        self.timer = 10
                        no_t.base_colour = "black"
                        min_1.base_colour = "black"
                        min_5.base_colour = "black"
                        min_10.base_colour = "blue"
                    if on.checkForInput(mouse_pos):
                        self.eval_bar = True
                        on.base_colour = "blue"
                        off.base_colour = "black"
                    elif off.checkForInput(mouse_pos):
                        self.eval_bar = False
                        on.base_colour = "black"
                        off.base_colour = "blue"
                    if confirm.checkForInput(mouse_pos):
                        self.mainloop()
                    

            pygame.display.update()

    def end_screen(self):
        pygame.display.set_caption("End Screen Menu")  
        screen = self.screen

        while True:
            screen.fill("white")
            options_text = self.font_40.render("GAME OVER", True, "#b68f40")
            options_rect = options_text.get_rect(center=(250,35))
            rect = (65, 5, 370, 60)
            pygame.draw.rect(screen, pygame.Color("black"), rect)
            screen.blit(options_text, options_rect)
            text = self.winner + " WINS"
            winner_text = self.font_20.render(text, True, "#b68f40")
            winner_rect = winner_text.get_rect(center=(250,100))
            win_rect = (125, 75, 250, 50)
            pygame.draw.rect(screen, pygame.Color("black"), win_rect)
            screen.blit(winner_text, winner_rect)
                

            mouse_pos = pygame.mouse.get_pos()        
            play_button = Button(image=self.rectangle_img, pos=(250, 200), 
                            text_input="PLAY AGAIN", font=self.font_18, base_colour="black", hovering_colour="White")
            quit_button = Button(image=self.rectangle_img, pos=(250, 300), 
                            text_input="QUIT", font=self.font_30, base_colour="black", hovering_colour="White")

            for button in [play_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(screen)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.game_mode()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()


    def mainloop(self):
        pygame.display.set_caption("Chess") 
        screen = self.screen
        start_pieces = self.start_pieces
        game = Game(start_pieces, eval_bar=self.eval_bar, timer_minutes=self.timer)
        board = game.board
        dragger = game.dragger
        
        if self.g_mode == "2":
            while True:
                # show methods
                screen.fill("white")
                game.show_bg(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_captured_pieces(screen)
                game.show_evaluation_bar(screen)
                
                # Check timer and display
                time_expired = game.show_timer(screen)
                if time_expired:
                    # Time ran out - opponent wins
                    expired_player = game.next_player
                    self.winner = "WHITE" if expired_player == "white" else "BLACK"
                    self.end_screen()
                    break

                if dragger.dragging:
                    dragger.update_blit(screen)
                
                

                for event in pygame.event.get():


                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQUARE_SIZE
                        clicked_col = dragger.mouseX // SQUARE_SIZE

                        # if clicked square has a piece ?
                        if clicked_row >= 0 and clicked_row <= 7:
                            if clicked_col >= 0 and clicked_col <= 7:
                                if board.squares[clicked_row][clicked_col].has_piece():
                                    piece = board.squares[clicked_row][clicked_col].piece
                                    piece.clear_moves()
                                    # valid piece (colour) ?
                                    if piece.colour == game.next_player:
                                        board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                        dragger.save_initial(event.pos)
                                        dragger.drag_piece(piece)
                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQUARE_SIZE
                            released_col = dragger.mouseX // SQUARE_SIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                captured = board.move(dragger.piece, move)
                                board.set_true_en_passant(dragger.piece)
                                # Track captured piece
                                if captured:
                                    game.add_captured_piece(captured)
                                # next turn
                                game.next_turn()
                                if game.checkmate():
                                    self.winner = "WHITE" if game.next_player == "black" else "BLACK"
                                    self.end_screen()

                                

                        dragger.undrag_piece()

                    # quit application
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
            
                
                pygame.display.update()
        elif self.g_mode == "computer":
            # Initialize engine with depth 2
            engine = Engine(depth=2)
            computer_moved = False
            # Pass player colour so timer only runs for human player
            game.player_colour = start_pieces

            while True:
                # Computer's turn - use engine to find best move
                if game.next_player != start_pieces and not computer_moved:
                    computer_colour = "black" if start_pieces == "white" else "white"
                    best_move = engine.search(board, computer_colour)
                    
                    if best_move:
                        piece, move = best_move
                        # Find the actual piece on the board
                        actual_piece = board.squares[move.initial.row][move.initial.col].piece
                        if actual_piece:
                            # Recalculate moves for the piece
                            actual_piece.clear_moves()
                            board.calc_moves(actual_piece, move.initial.row, move.initial.col, bool=True)
                            
                            # Find the matching move
                            valid_move = None
                            for m in actual_piece.moves:
                                if m.final.row == move.final.row and m.final.col == move.final.col:
                                    valid_move = m
                                    break
                            
                            if valid_move and board.valid_move(actual_piece, valid_move):
                                captured = board.move(actual_piece, valid_move)
                                board.set_true_en_passant(actual_piece)
                                # Track captured piece
                                if captured:
                                    game.add_captured_piece(captured)
                                # next turn
                                game.next_turn()
                                computer_moved = True
                                if game.checkmate():
                                    self.winner = "COMPUTER"
                                    self.end_screen()
                                    return
                
                # show methods
                screen.fill("white")
                game.show_bg(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_captured_pieces(screen)
                game.show_evaluation_bar(screen)
                
                # Check timer and display
                time_expired = game.show_timer(screen)
                if time_expired:
                    # Time ran out - opponent wins
                    expired_player = game.next_player
                    self.winner = "WHITE" if expired_player == "white" else "BLACK"
                    self.end_screen()
                    break

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():



                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if game.next_player == start_pieces:
                            dragger.update_mouse(event.pos)

                            clicked_row = dragger.mouseY // SQUARE_SIZE
                            clicked_col = dragger.mouseX // SQUARE_SIZE

                            # if clicked square has a piece ?
                            if clicked_row >= 0 and clicked_row <= 7:
                                if clicked_col >= 0 and clicked_col <= 7:
                                    if board.squares[clicked_row][clicked_col].has_piece():
                                        piece = board.squares[clicked_row][clicked_col].piece
                                        piece.clear_moves()
                                        # valid piece (colour) ?
                                        if piece.colour == start_pieces:
                                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                            dragger.save_initial(event.pos)
                                            dragger.drag_piece(piece)
                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQUARE_SIZE
                            released_col = dragger.mouseX // SQUARE_SIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                captured = board.move(dragger.piece, move)
                                board.set_true_en_passant(dragger.piece)
                                # Track captured piece
                                if captured:
                                    game.add_captured_piece(captured)
                                # next turn
                                game.next_turn()
                                computer_moved = False  # Reset flag for computer's next move
                                if game.checkmate():
                                    self.winner = "PLAYER"
                                    self.end_screen()
                                    return

                        dragger.undrag_piece()

                    # quit application
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
            
                
                pygame.display.update()


main = Main()
main.main_menu()