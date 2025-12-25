import pygame
import os
import time
from constants import *
from board import Board
from dragger import Dragger
from engine import Engine

class Game:
    # Class-level image cache for piece textures
    _image_cache = {}

    def __init__(self, start_pieces, eval_bar=False, timer_minutes=0, player_colour=None):
        self.next_player = "white"
        self.start_pieces = start_pieces
        self.board = Board(start_pieces)
        self.dragger = Dragger()
        # Track captured pieces: {colour: {piece_name: count}}
        self.captured_pieces = {"white": {}, "black": {}}
        # Evaluation bar setting
        self.eval_bar = eval_bar
        # Engine for evaluation (lazy initialization)
        self._engine = None
        # Timer settings
        self.timer_minutes = timer_minutes
        self.timer_enabled = timer_minutes > 0
        # Player colour (for computer mode - only run timer for human player)
        self.player_colour = player_colour
        # Time remaining in seconds for each player
        self.time_remaining = {
            "white": timer_minutes * 60 if timer_minutes > 0 else 0,
            "black": timer_minutes * 60 if timer_minutes > 0 else 0
        }
        # Track last update time for timer - initialize when timer is enabled
        if self.timer_enabled:
            self.last_time_update = time.time()
        else:
            self.last_time_update = None

    @classmethod
    def get_cached_image(cls, texture_path, size):
        """Get cached image or load and cache it"""
        cache_key = (texture_path, size)
        if cache_key not in cls._image_cache:
            cls._image_cache[cache_key] = pygame.transform.scale(
                pygame.image.load(texture_path), (size, size)
            )
        return cls._image_cache[cache_key]


    # blit methods

    def show_bg(self, surface):
        
        for row in range(ROWS):
            for col in range(COLS):
                # colour
                colour = pygame.Color("white") if (row + col) % 2 == 0 else (119, 154, 88)
                # rect
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, colour, rect)



    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        img = self.get_cached_image(piece.texture, SQUARE_SIZE)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # colour
                colour = pygame.Color("red")
                # rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, colour, rect)
    
    def show_captured_pieces(self, surface):
        """Display captured pieces below the board"""
        # Piece order for display (most valuable first)
        piece_order = ["queen", "rook", "bishop", "knight", "pawn"]
        piece_size = 25  # Smaller size to fit in available space
        
        # Try to load font, fallback to default if not available
        try:
            font = pygame.font.Font("font.ttf", 16)
        except:
            font = pygame.font.Font(None, 16)
        
        # White captured pieces (top row, below board)
        white_y = HEIGHT + 5
        white_x = 10
        for piece_name in piece_order:
            if piece_name in self.captured_pieces["white"]:
                count = self.captured_pieces["white"][piece_name]
                if count > 0:
                    # Load and display piece image
                    texture_path = os.path.join("images", f"white_{piece_name}.png")
                    try:
                        img = self.get_cached_image(texture_path, piece_size)
                        surface.blit(img, (white_x, white_y))
                        
                        # Display count
                        count_text = font.render(f"x{count}", True, pygame.Color("black"))
                        surface.blit(count_text, (white_x + piece_size + 3, white_y + piece_size // 2 - 7))
                        
                        white_x += piece_size + 35  # Space for piece and count
                    except Exception as e:
                        # If image fails, just show text
                        count_text = font.render(f"{piece_name}: {count}", True, pygame.Color("black"))
                        surface.blit(count_text, (white_x, white_y))
                        white_x += 80
        
        # Black captured pieces (bottom row, below white pieces)
        black_y = HEIGHT + 35
        black_x = 10
        for piece_name in piece_order:
            if piece_name in self.captured_pieces["black"]:
                count = self.captured_pieces["black"][piece_name]
                if count > 0:
                    # Load and display piece image
                    texture_path = os.path.join("images", f"black_{piece_name}.png")
                    try:
                        img = self.get_cached_image(texture_path, piece_size)
                        surface.blit(img, (black_x, black_y))
                        
                        # Display count
                        count_text = font.render(f"x{count}", True, pygame.Color("black"))
                        surface.blit(count_text, (black_x + piece_size + 3, black_y + piece_size // 2 - 7))
                        
                        black_x += piece_size + 35  # Space for piece and count
                    except Exception as e:
                        # If image fails, just show text
                        count_text = font.render(f"{piece_name}: {count}", True, pygame.Color("black"))
                        surface.blit(count_text, (black_x, black_y))
                        black_x += 80
    
    def add_captured_piece(self, piece):
        """Add a captured piece to the tracking dictionary"""
        if piece is None:
            return
        
        colour = piece.colour
        piece_name = piece.name
        
        if piece_name not in self.captured_pieces[colour]:
            self.captured_pieces[colour][piece_name] = 0
        self.captured_pieces[colour][piece_name] += 1
    
    def _get_engine(self):
        """Lazy initialization of engine for evaluation"""
        if self._engine is None:
            self._engine = Engine(depth=1)  # Only need evaluation, not search
        return self._engine
    
    def show_evaluation_bar(self, surface):
        """Display evaluation bar on the right side of the board"""
        if not self.eval_bar:
            return
        
        # Bar dimensions and position
        bar_width = 20
        bar_height = HEIGHT
        bar_x = WIDTH + 10  # Right side of board
        bar_y = 0
        
        # Get current position evaluation
        engine = self._get_engine()
        # Evaluate from white's perspective
        evaluation = engine._fast_evaluate(self.board, "white")
        
        # Normalize evaluation to -1.0 to 1.0 range (clamp to reasonable values)
        # Typical chess evaluation range: -20 to +20 (pawn units)
        max_eval = 20.0
        normalized = max(-1.0, min(1.0, evaluation / max_eval))
        
        # Calculate bar fill
        # Positive (white advantage) fills from top, negative (black advantage) from bottom
        center_y = bar_y + bar_height // 2
        
        if normalized >= 0:
            # White advantage - fill from center upward
            fill_height = int(bar_height // 2 * normalized)
            fill_y = center_y - fill_height
            fill_color = pygame.Color(240, 240, 240)  # Light gray for white
        else:
            # Black advantage - fill from center downward
            fill_height = int(bar_height // 2 * abs(normalized))
            fill_y = center_y
            fill_color = pygame.Color(50, 50, 50)  # Dark gray for black
        
        # Draw background (neutral)
        pygame.draw.rect(surface, pygame.Color(200, 200, 200), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Draw center line
        pygame.draw.line(surface, pygame.Color(100, 100, 100), 
                        (bar_x, center_y), (bar_x + bar_width, center_y), 2)
        
        # Draw evaluation fill
        if abs(normalized) > 0.01:  # Only draw if significant
            if normalized >= 0:
                pygame.draw.rect(surface, fill_color, 
                               (bar_x, fill_y, bar_width, fill_height))
            else:
                pygame.draw.rect(surface, fill_color, 
                               (bar_x, fill_y, bar_width, fill_height))
        
        # Draw border
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Display evaluation text (optional, below the bar)
        try:
            font = pygame.font.Font("font.ttf", 12)
        except:
            font = pygame.font.Font(None, 12)
        
        # Format evaluation (show in pawns)
        eval_text = f"{evaluation:+.1f}"
        text_surface = font.render(eval_text, True, pygame.Color("black"))
        text_x = bar_x + bar_width // 2 - text_surface.get_width() // 2
        text_y = bar_height + 5
        surface.blit(text_surface, (text_x, text_y))

    # other methods

    def next_turn(self):
        # Stop timer for current player before switching turns
        if self.timer_enabled:
            self._update_timer()
            # Stop timer - it will restart when show_timer is called for the new player
            self.last_time_update = None
        
        self.next_player = "white" if self.next_player == "black" else "black"
        
        # Timer will restart when show_timer is called for the new player
    
    def _update_timer(self):
        """Update timer countdown for current player"""
        if not self.timer_enabled or self.last_time_update is None:
            return
        
        current_time = time.time()
        elapsed = current_time - self.last_time_update
        
        # Decrease time for the player whose turn just ended
        previous_player = "black" if self.next_player == "white" else "white"
        self.time_remaining[previous_player] -= elapsed
        
        # Check if time ran out
        if self.time_remaining[previous_player] <= 0:
            self.time_remaining[previous_player] = 0
    
    def update_timer_during_turn(self):
        """Update timer during the current player's turn only (only for human player in computer mode)"""
        if not self.timer_enabled:
            return False
        
        # Only update if it's the current player's turn
        current_player = self.next_player
        
        # In computer mode, only run timer for the human player
        if self.player_colour is not None and current_player != self.player_colour:
            # It's computer's turn, don't run timer
            self.last_time_update = None
            return False
        
        if self.last_time_update is None:
            self.last_time_update = time.time()
            return False
        
        current_time = time.time()
        elapsed = current_time - self.last_time_update
        
        # Only count down for the current player
        self.time_remaining[current_player] -= elapsed
        
        # Update last time
        self.last_time_update = current_time
        
        # Check if time ran out
        if self.time_remaining[current_player] <= 0:
            self.time_remaining[current_player] = 0
            return True  # Time expired
        return False
    
    def get_time_remaining(self, colour):
        """Get time remaining for a player in seconds"""
        return max(0, self.time_remaining[colour])
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def show_timer(self, surface):
        """Display timer for current player in bottom right (only shows/runs for human player in computer mode)"""
        if not self.timer_enabled:
            return False
        
        # Try to load font
        try:
            font = pygame.font.Font("font.ttf", 24)
        except:
            font = pygame.font.Font(None, 24)
        
        # Only update timer for the current player whose turn it is (and only if it's human player in computer mode)
        time_expired = self.update_timer_during_turn()
        
        # Get current player's time
        current_player = self.next_player
        
        # In computer mode, only show timer when it's the human player's turn
        if self.player_colour is not None and current_player != self.player_colour:
            # It's computer's turn, don't display timer
            return False
        
        current_time = self.get_time_remaining(current_player)
        
        # Display timer in bottom right of screen (outside the board)
        timer_text = font.render(self.format_time(current_time), True, 
                                pygame.Color("red") if current_time < 10 else pygame.Color("black"))
        timer_rect = timer_text.get_rect()
        # Position in bottom right of screen (screen is 500x500, board is 400x400)
        # Place it in the bottom right corner of the screen
        screen_width = 500
        screen_height = 500
        timer_rect.bottomright = (screen_width - 10, screen_height - 10)
        surface.blit(timer_text, timer_rect)
        
        return time_expired


    def checkmate(self):
        m = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_team_piece(self.next_player):
                    p = self.board.squares[row][col].piece
                    p.clear_moves()
                    self.board.calc_moves(p, row, col, bool=True)
                    if len(p.moves) > 0:
                        m = m + 1
        if m == 0:
            return True
        
        return False


    def reset(self):
        self.__init__()