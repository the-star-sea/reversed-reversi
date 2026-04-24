# Reversed Reversi

## Overview
A strategic twist on the classic Reversi (Othello) board game. The objective is inverted: players aim to have the *fewest* pieces on the board by the end of the game.

## Features
- Complete game logic implementation for the reversed rule set (`game_logic.py`).
- Multiple AI difficulty levels:
  - **Basic** (`ai_basic.py`)
  - **Advanced** (`ai_advanced.py`)
  - **Expert** (`ai_expert.py` - uses Minimax with alpha-beta pruning and heuristic evaluation)
- Automated testing harness (`auto_test.py`) to benchmark AI performance.

## Setup & Usage
Requires Python 3.
```bash
python3 control.py
```
To run automated AI matches:
```bash
python3 auto_test.py
```

## Highlights
- Custom heuristic evaluation functions specifically tuned for the 'reversed' objective (e.g., prioritizing forced moves and corner avoidance).
- Modular AI design making it easy to plug in new algorithms.

## Limitations
- Command-line interface only; lacks a graphical UI.
- Search depth for the Expert AI is constrained by Python's single-threaded execution speed.
