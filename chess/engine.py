import copy
from constants import *
from board import Board
from square import Square
from move import Move
from piece import *

class Engine:
    # Transposition table for caching evaluated positions
    _transposition_table = {}
    _table_size = 10000  # Limit table size to prevent memory issues
    
    # Piece-square tables for positional evaluation
    # Values are from white's perspective (row 0-7, col 0-7)
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
        [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
        [0,  0,  0,  0.2, 0.2,  0,  0,  0],
        [0.05, -0.05, -0.1,  0,  0, -0.1, -0.05, 0.05],
        [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]
    
    KNIGHT_TABLE = [
        [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
        [-0.4, -0.2,  0,  0,  0,  0, -0.2, -0.4],
        [-0.3,  0, 0.1, 0.15, 0.15, 0.1,  0, -0.3],
        [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
        [-0.3,  0, 0.15, 0.2, 0.2, 0.15,  0, -0.3],
        [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
        [-0.4, -0.2,  0, 0.05, 0.05,  0, -0.2, -0.4],
        [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
    ]
    
    BISHOP_TABLE = [
        [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
        [-0.1,  0,  0,  0,  0,  0,  0, -0.1],
        [-0.1,  0, 0.05, 0.1, 0.1, 0.05,  0, -0.1],
        [-0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1],
        [-0.1,  0, 0.1, 0.1, 0.1, 0.1,  0, -0.1],
        [-0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
        [-0.1, 0.05,  0,  0,  0,  0, 0.05, -0.1],
        [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
    ]
    
    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
        [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
        [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
        [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
        [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
        [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
        [0,  0,  0, 0.05, 0.05,  0,  0,  0]
    ]
    
    QUEEN_TABLE = [
        [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
        [-0.1,  0,  0,  0,  0,  0,  0, -0.1],
        [-0.1,  0, 0.05, 0.05, 0.05, 0.05,  0, -0.1],
        [-0.05,  0, 0.05, 0.05, 0.05, 0.05,  0, -0.05],
        [0,  0, 0.05, 0.05, 0.05, 0.05,  0,  0],
        [-0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, -0.1],
        [-0.1,  0, 0.05,  0,  0, 0.05,  0, -0.1],
        [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
    ]
    
    KING_TABLE_MIDDLE = [
        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
        [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
        [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
        [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
        [0.2, 0.2,  0,  0,  0,  0, 0.2, 0.2],
        [0.2, 0.3, 0.1,  0,  0, 0.1, 0.3, 0.2]
    ]
    
    def __init__(self, depth=2):
        """
        Initialize the chess engine:
        - depth: Main search depth (default: 2)
        """
        self.depth = depth
        # Clear transposition table for new game
        Engine._transposition_table.clear()
    
    def search(self, board, colour, depth=None):
        """
        Simple minimax search with alpha-beta pruning
        Returns the best move for the given colour
        """
        if depth is None:
            depth = self.depth
        
        # Get all possible moves
        all_moves = self._get_all_moves(board, colour)
        
        if not all_moves:
            return None
        
        # Order moves for better alpha-beta pruning
        all_moves = self._order_moves(board, all_moves)
        
        best_move = None
        best_value = float('-inf') if colour == "white" else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for piece, move in all_moves:
            # Make the move on a copy of the board
            temp_board = copy.deepcopy(board)
            
            # Get the piece directly from the copied board using move coordinates
            if not temp_board.squares[move.initial.row][move.initial.col].has_piece():
                continue
            
            temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
            
            # Verify it's the right piece
            if temp_piece.name != piece.name or temp_piece.colour != piece.colour:
                continue
            
            # Calculate moves for the temp piece
            temp_piece.clear_moves()
            temp_board.calc_moves(temp_piece, move.initial.row, move.initial.col, bool=True)
            
            # Find the corresponding move
            temp_move = None
            for m in temp_piece.moves:
                if m.final.row == move.final.row and m.final.col == move.final.col:
                    temp_move = m
                    break
            
            if not temp_move:
                continue
            
            # Make the move
            temp_board.move(temp_piece, temp_move)
            temp_board.set_true_en_passant(temp_piece)
            
            # Evaluate the position
            if depth == 1:
                # Direct evaluation at leaf nodes
                value = self._fast_evaluate(temp_board, colour)
            else:
                # Recursive search
                opponent_colour = "black" if colour == "white" else "white"
                _, value = self._minimax(temp_board, opponent_colour, depth - 1, alpha, beta, False)
            
            # Update best move
            if colour == "white":
                if value > best_value:
                    best_value = value
                    best_move = (piece, move)
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = (piece, move)
                beta = min(beta, value)
            
            # Alpha-beta pruning
            if alpha >= beta:
                break
        
        return best_move
    
    def _minimax(self, board, colour, depth, alpha, beta, maximizing):
        """
        Minimax algorithm with alpha-beta pruning
        """
        if depth == 0:
            # Direct evaluation at leaf nodes
            return None, self._fast_evaluate(board, "white" if maximizing else "black")
        
        all_moves = self._get_all_moves(board, colour)
        
        if not all_moves:
            # Checkmate or stalemate - evaluate endgame
            eval_score = self.evaluate(board, "white" if maximizing else "black")
            # Penalize checkmate heavily
            if self._is_in_check(board, colour):
                eval_score = float('-inf') if maximizing else float('inf')
            return None, eval_score
        
        # Order moves for better pruning
        all_moves = self._order_moves(board, all_moves)
        
        if maximizing:
            max_value = float('-inf')
            best_move = None
            
            for piece, move in all_moves:
                temp_board = copy.deepcopy(board)
                
                # Get the piece directly from the copied board
                if not temp_board.squares[move.initial.row][move.initial.col].has_piece():
                    continue
                
                temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
                
                # Verify it's the right piece
                if temp_piece.name != piece.name or temp_piece.colour != piece.colour:
                    continue
                
                temp_piece.clear_moves()
                temp_board.calc_moves(temp_piece, move.initial.row, move.initial.col, bool=True)
                
                temp_move = self._find_move_in_piece(temp_piece, move.final.row, move.final.col)
                if not temp_move:
                    continue
                
                temp_board.move(temp_piece, temp_move)
                temp_board.set_true_en_passant(temp_piece)
                
                opponent_colour = "black" if colour == "white" else "white"
                _, value = self._minimax(temp_board, opponent_colour, depth - 1, alpha, beta, False)
                
                if value > max_value:
                    max_value = value
                    best_move = (piece, move)
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            
            return best_move, max_value
        else:
            min_value = float('inf')
            best_move = None
            
            for piece, move in all_moves:
                temp_board = copy.deepcopy(board)
                
                # Get the piece directly from the copied board
                if not temp_board.squares[move.initial.row][move.initial.col].has_piece():
                    continue
                
                temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
                
                # Verify it's the right piece
                if temp_piece.name != piece.name or temp_piece.colour != piece.colour:
                    continue
                
                temp_piece.clear_moves()
                temp_board.calc_moves(temp_piece, move.initial.row, move.initial.col, bool=True)
                
                temp_move = self._find_move_in_piece(temp_piece, move.final.row, move.final.col)
                if not temp_move:
                    continue
                
                temp_board.move(temp_piece, temp_move)
                temp_board.set_true_en_passant(temp_piece)
                
                opponent_colour = "black" if colour == "white" else "white"
                _, value = self._minimax(temp_board, opponent_colour, depth - 1, alpha, beta, True)
                
                if value < min_value:
                    min_value = value
                    best_move = (piece, move)
                
                beta = min(beta, value)
                if beta <= alpha:
                    break
            
            return best_move, min_value
    
    def _order_moves(self, board, moves):
        """
        Order moves to improve alpha-beta pruning efficiency
        Captures first (sorted by MVV-LVA), then checks, then other moves
        """
        capture_moves = []
        check_moves = []
        other_moves = []
        
        for piece, move in moves:
            # Check if move is a capture
            if board.squares[move.final.row][move.final.col].has_piece():
                # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
                captured_piece = board.squares[move.final.row][move.final.col].piece
                capture_value = abs(captured_piece.value) - abs(piece.value)
                capture_moves.append((capture_value, piece, move))
            else:
                # Check if move gives check (simplified check)
                # This is a heuristic - we'll check if it's likely a check
                other_moves.append((piece, move))
        
        # Sort captures by value (highest first) - MVV-LVA ordering
        capture_moves.sort(key=lambda x: x[0], reverse=True)
        
        # Combine: captures first, then checks, then other moves
        ordered = [(p, m) for _, p, m in capture_moves] + check_moves + other_moves
        return ordered
    
    def _get_all_moves(self, board, colour):
        """
        Get all possible moves for a given colour
        Returns list of (piece, move) tuples
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.colour == colour:
                        piece.clear_moves()
                        board.calc_moves(piece, row, col, bool=True)
                        for move in piece.moves:
                            moves.append((piece, move))
        return moves
    
    def _find_move_in_piece(self, piece, final_row, final_col):
        """Find move with matching final position"""
        for move in piece.moves:
            if move.final.row == final_row and move.final.col == final_col:
                return move
        return None
    
    def _find_king(self, board, colour):
        """Find and cache king position"""
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if isinstance(piece, King) and piece.colour == colour:
                        return row, col
        return None, None
    
    def _is_in_check(self, board, colour):
        """Check if the king of given colour is in check - optimized"""
        # Find the king
        king_row, king_col = self._find_king(board, colour)
        
        if king_row is None:
            return False
        
        # Check if any enemy piece can attack the king
        opponent_colour = "black" if colour == "white" else "white"
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.colour == opponent_colour:
                        # Quick check for direct attacks (without full move calculation)
                        if self._can_attack_square(board, piece, row, col, king_row, king_col):
                            return True
        
        return False
    
    def _can_attack_square(self, board, piece, piece_row, piece_col, target_row, target_col):
        """Quick check if piece can attack target square without full move calculation"""
        # Only calculate moves if necessary
        if not piece.moves:
            piece.clear_moves()
            board.calc_moves(piece, piece_row, piece_col, bool=False)
        
        for move in piece.moves:
            if move.final.row == target_row and move.final.col == target_col:
                return True
        return False
    
    def _get_piece_square_value(self, piece, row, col):
        """Get positional value from piece-square table"""
        # Flip row for black pieces (black's perspective)
        if piece.colour == "black":
            row = 7 - row
        
        if isinstance(piece, Pawn):
            return self.PAWN_TABLE[row][col]
        elif isinstance(piece, Knight):
            return self.KNIGHT_TABLE[row][col]
        elif isinstance(piece, Bishop):
            return self.BISHOP_TABLE[row][col]
        elif isinstance(piece, Rook):
            return self.ROOK_TABLE[row][col]
        elif isinstance(piece, Queen):
            return self.QUEEN_TABLE[row][col]
        elif isinstance(piece, King):
            return self.KING_TABLE_MIDDLE[row][col]
        return 0
    
    def _evaluate_pawn_structure(self, board, colour):
        """Evaluate pawn structure - simplified for speed"""
        score = 0
        pawns = []
        pawn_cols = {}  # Track pawns per column
        
        # Collect pawn positions (single pass)
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if isinstance(piece, Pawn) and piece.colour == colour:
                        pawns.append((row, col))
                        if col not in pawn_cols:
                            pawn_cols[col] = []
                        pawn_cols[col].append(row)
        
        # Doubled pawns penalty (simplified)
        for col, rows in pawn_cols.items():
            if len(rows) > 1:
                score -= 0.3 * (len(rows) - 1)
        
        # Simplified isolated pawns check
        for row, col in pawns:
            # Check adjacent files
            has_adjacent = False
            for adj_col in [col - 1, col + 1]:
                if 0 <= adj_col < 8 and adj_col in pawn_cols:
                    has_adjacent = True
                    break
            if not has_adjacent:
                score -= 0.2
        
        # Simplified passed pawns (only check immediate squares)
        for row, col in pawns:
            opponent_dir = 1 if colour == "white" else -1
            next_row = row + opponent_dir
            if 0 <= next_row < 8:
                # Check if opponent has pawns blocking
                blocked = False
                for check_col in [col - 1, col, col + 1]:
                    if 0 <= check_col < 8:
                        if board.squares[next_row][check_col].has_piece():
                            p = board.squares[next_row][check_col].piece
                            if isinstance(p, Pawn) and p.colour != colour:
                                blocked = True
                                break
                if not blocked:
                    # Bonus for advancing pawns
                    advance_bonus = (7 - row) * 0.2 if colour == "white" else row * 0.2
                    score += advance_bonus
        
        return score
    
    def _evaluate_mobility(self, board, colour):
        """Evaluate piece mobility (number of legal moves) - optimized version"""
        mobility = 0
        # Cache move counts to avoid recalculating
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.colour == colour:
                        # Only calculate if moves haven't been calculated
                        if not piece.moves:
                            piece.clear_moves()
                            board.calc_moves(piece, row, col, bool=True)
                        move_count = len(piece.moves)
                        # Different pieces have different mobility values
                        if isinstance(piece, Pawn):
                            mobility += move_count * 0.1
                        elif isinstance(piece, Knight) or isinstance(piece, Bishop):
                            mobility += move_count * 0.15
                        elif isinstance(piece, Rook):
                            mobility += move_count * 0.2
                        elif isinstance(piece, Queen):
                            mobility += move_count * 0.25
        return mobility
    
    def _evaluate_king_safety(self, board, colour):
        """Evaluate king safety - optimized"""
        score = 0
        
        # Find the king (use cached method)
        king_row, king_col = self._find_king(board, colour)
        
        if king_row is None:
            return 0
        
        # Count friendly pieces near the king (pawn shield)
        friendly_near_king = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                check_row = king_row + dr
                check_col = king_col + dc
                if 0 <= check_row < 8 and 0 <= check_col < 8:
                    if board.squares[check_row][check_col].has_piece():
                        piece = board.squares[check_row][check_col].piece
                        if piece.colour == colour:
                            friendly_near_king += 0.1
        
        score += friendly_near_king
        
        # Penalty if king is exposed (no pawns in front)
        if colour == "white":
            if king_row > 0:
                if not board.squares[king_row - 1][king_col].has_piece() or \
                   not isinstance(board.squares[king_row - 1][king_col].piece, Pawn):
                    score -= 0.2
        else:
            if king_row < 7:
                if not board.squares[king_row + 1][king_col].has_piece() or \
                   not isinstance(board.squares[king_row + 1][king_col].piece, Pawn):
                    score -= 0.2
        
        return score
    
    def _fast_evaluate(self, board, colour):
        """
        Fast evaluation - only material and basic position
        """
        score = 0
        white_material = 0
        black_material = 0
        
        # Material and basic positional evaluation
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    
                    # Material value
                    if piece.colour == "white":
                        white_material += abs(piece.value)
                    else:
                        black_material += abs(piece.value)
                    
                    # Basic positional value
                    pos_value = self._get_piece_square_value(piece, row, col)
                    if piece.colour == "white":
                        score += pos_value
                    else:
                        score -= pos_value
        
        # Material difference
        material_diff = white_material - black_material
        score += material_diff
        
        # Return score from the perspective of the given colour
        if colour == "white":
            return score
        else:
            return -score
    
    def evaluate(self, board, colour):
        """
        Comprehensive evaluation function
        Positive values favor white, negative favor black
        """
        score = 0
        
        # Material evaluation
        white_material = 0
        black_material = 0
        
        # Positional and material evaluation
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    
                    # Material value
                    if piece.colour == "white":
                        white_material += abs(piece.value)
                    else:
                        black_material += abs(piece.value)
                    
                    # Positional value from piece-square tables
                    pos_value = self._get_piece_square_value(piece, row, col)
                    if piece.colour == "white":
                        score += pos_value
                    else:
                        score -= pos_value
        
        # Material difference
        material_diff = white_material - black_material
        score += material_diff
        
        # Only evaluate expensive features at root or when needed
        # Pawn structure evaluation (expensive, so we'll make it optional)
        white_pawn_structure = self._evaluate_pawn_structure(board, "white")
        black_pawn_structure = self._evaluate_pawn_structure(board, "black")
        score += white_pawn_structure - black_pawn_structure
        
        # Mobility evaluation (expensive)
        white_mobility = self._evaluate_mobility(board, "white")
        black_mobility = self._evaluate_mobility(board, "black")
        score += white_mobility - black_mobility
        
        # King safety
        white_king_safety = self._evaluate_king_safety(board, "white")
        black_king_safety = self._evaluate_king_safety(board, "black")
        score += white_king_safety - black_king_safety
        
        # Check bonus/penalty
        if self._is_in_check(board, "black"):
            score += 0.5  # White has opponent in check
        if self._is_in_check(board, "white"):
            score -= 0.5  # Black has opponent in check
        
        # Return score from the perspective of the given colour
        if colour == "white":
            return score
        else:
            return -score
