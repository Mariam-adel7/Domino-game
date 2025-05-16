### 👢 Domino Game (Pygame)

A two-player Domino game built with Python and Pygame. This game allows two players to take turns placing dominoes on the board according to classic rules, with interactive graphics and basic scoring.

---

## 🎮 Features

* Graphical user interface using `pygame`
* Two-player local game logic
* Automatically checks valid moves
* Option to draw a domino if no move is available
* Win detection and score display for remaining tiles

---

## 💠 Requirements

* Python 3.x
* [Pygame](https://www.pygame.org/) library

You can install Pygame via pip:

```bash
pip install pygame
```

---

## ▶️ How to Run

1. Clone or download this repository.
2. Run the Python file:

```bash
python Domino-game.py
```

Make sure you're in the same directory as `Domino-game.py`.

---

## 🧹 Game Rules (Simplified)

* Each player starts with 7 random dominoes.
* The board starts empty. Any tile can be placed first.
* Players alternate turns placing a domino that matches either open end.
* If no valid move is available, the player must draw one tile (if available).
* First player to place all tiles wins.
* The winner’s score is the sum of remaining tiles in the opponent’s hand.
