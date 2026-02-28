# ♟️ Python Chess Engine (Pygame)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)
![Status](https://img.shields.io/badge/Status-Playable-success.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-orange.svg)

A fully playable chess game built in **Python using Pygame**, featuring legal move validation, check & checkmate detection, undo functionality, and animated checkmate effects.

---

## 🚀 Features

### ♜ Core Chess Logic
- ✅ Standard 8x8 chess board
- ✅ Full legal move generation
- ✅ Turn-based system (White / Black)
- ✅ Move validation (illegal moves blocked)
- ✅ King position tracking

### 👑 Game State Handling
- ✅ Check detection
- ✅ Checkmate detection
- ✅ Stalemate detection
- ✅ Undo move (Z key)
- ✅ Restart game (R key)
- ✅ Move history tracking

### 🎨 UI Features
- ✅ Piece selection highlight
- ✅ Legal move highlight
- ✅ Capture highlight
- ✅ King glows red when in check
- ✅ Animated checkmate screen:
  - Dark fade overlay
  - Losing king glow
  - Zooming "CHECKMATE" text
  - Restart prompt

---

## 🎮 Controls

| Action | Key |
|--------|-----|
| Select / Move Piece | Mouse Click |
| Undo Move | Z |
| Restart Game | R |
| Quit | Close Window |

---

## 🗂️ Project Structure

```
Chess/
│
├── ChessMain.py        # UI, rendering, input handling, animations
├── ChessEngine.py      # Core game logic and rules
├── images/             # Piece images
│   ├── wp.png
│   ├── wR.png
│   ├── ...
│   └── bK.png
└── README.md
```

---

## 🛠️ Requirements

- Python 3.8+
- Pygame 2.x

Install pygame:

```bash
pip install pygame
```

---

## ▶️ How To Run

Navigate into the project folder and run:

```bash
python ChessMain.py
```

---

## ⚙️ How It Works

### ♟ GameState (ChessEngine.py)

Handles:
- Board representation
- Move generation
- Legal move filtering
- Check detection
- Checkmate & stalemate logic
- Undo functionality

### 🎮 ChessMain (UI Layer)

Handles:
- Rendering board & pieces
- Mouse and keyboard input
- Highlight effects
- Animation system
- Checkmate animation overlay

---

## 🧠 Engine Architecture

- Board stored as a 2D list
- Moves represented using a `Move` class
- Legal move filtering simulates moves and checks king safety
- Checkmate occurs when:
  - No valid moves remain
  - King is in check

---

## 🎬 Animation System

The checkmate animation includes:
- Smooth fade-to-dark overlay
- Red glow on losing king
- Dynamic text zoom
- Restart prompt

---

## 📌 Current Limitations

- ❌ No castling
- ❌ No pawn promotion UI
- ❌ No en passant
- ❌ No AI opponent
- ❌ No timers or clock
- ❌ No PGN export

---

## 🔮 Future Improvements

Planned upgrades:

- ♜ Castling support
- ♛ Pawn promotion interface
- 🤖 Minimax AI opponent
- ⏱ Chess clock
- 🎵 Sound effects
- 🎨 Custom board themes
- 📄 PGN save/load
- ✨ Smooth move animations

---

## 🎓 Learning Outcomes

This project demonstrates:

- Object-Oriented Programming (OOP)
- Game state simulation
- Event-driven programming with Pygame
- Rule enforcement in board games
- Rendering loops & animations
- Clean separation of UI and logic

---

## 🏆 Project Status

✔ Fully playable  
✔ Stable  
✔ Clean architecture  
✔ No runtime errors  

---

## 📜 License

This project is for educational purposes.

---

Made with ❤️ using Python & Pygame.
