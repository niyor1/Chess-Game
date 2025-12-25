# Chess Game

A fully-featured chess game built with Python and Pygame, featuring both two-player and computer opponent modes.

## Features

- **Two Game Modes:**
  - 2-Player mode for local multiplayer
  - Computer mode with AI opponent (minimax algorithm with alpha-beta pruning)

- **Timer Options:**
  - No timer
  - 1 minute
  - 5 minutes
  - 10 minutes

- **Game Features:**
  - Full chess rules implementation (castling, en passant, pawn promotion)
  - Visual move indicators
  - Captured pieces display
  - Optional evaluation bar showing position assessment
  - Checkmate detection
  - Time control with automatic game end on timeout

- **User Interface:**
  - Clean, modern menu system
  - Drag-and-drop piece movement
  - Visual feedback for valid moves
  - Game over screen with winner announcement

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone or download this repository

2. Install Pygame (if not already installed):
   ```bash
   pip install pygame
   ```

## How to Run

Navigate to the `chess` directory and run:

```bash
python main.py
```

Or from the project root:

```bash
cd chess
python main.py
```

## How to Play

1. **Main Menu:** Select "PLAY" to start a game
2. **Game Mode:** Choose between "2-PLAYER" or "COMPUTER"
3. **Options (Computer Mode Only):**
   - Select your piece color (White or Black)
   - Choose timer duration (No Timer, 1 Minute, 5 Minutes, or 10 Minutes)
   - Toggle evaluation bar (ON/OFF)
   - Click "PLAY" to confirm
4. **Gameplay:**
   - Click and drag pieces to move them
   - Valid moves are highlighted in red
   - Captured pieces are displayed below the board
   - Timer (if enabled) is shown in the bottom right corner
   - The game ends on checkmate or timeout

## Project Structure

```
chess/
├── main.py          # Main entry point and menu system
├── game.py          # Game logic and rendering
├── board.py         # Chess board and move validation
├── piece.py         # Chess piece classes and movement rules
├── engine.py        # AI engine (minimax with alpha-beta pruning)
├── dragger.py       # Piece dragging functionality
├── move.py          # Move representation
├── square.py        # Square representation
├── button.py        # UI button component
├── constants.py     # Game constants
├── font.ttf         # Font file
└── images/          # Piece and UI images
    ├── white_*.png  # White piece images
    ├── black_*.png  # Black piece images
    └── *.png        # UI elements
```

## Technical Details

- **AI Engine:** Uses minimax algorithm with alpha-beta pruning for move selection
- **Evaluation:** Position evaluation based on material and piece-square tables
- **Move Generation:** Validates all chess rules including special moves (castling, en passant, promotion)
- **Performance:** Image caching and resource optimization for smooth gameplay

## License

This project is open source and available for educational purposes.

