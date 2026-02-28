"""
This is our main driver file.It will be responsible for handling user inputs and current Gamestate object
 """

import pygame as p
import ChessEngine


#Colors 
Peach = (255, 229, 180)
LightPeach = (255, 240, 220)
White= (255, 255, 255)
Ivory= (255, 255, 240)
LightBlue =	(173, 216, 230)
LightGreen =	(144, 238, 144)
LightPink =	(255, 182, 193)
LightYellow =	(255, 255, 224)
LightGray =	(211, 211, 211)
Lavender =	(230, 230, 250)
LightPink = (255, 182, 193)
PastelPink = (248, 200, 220)
Peach =  (255, 229, 180)
LightSalmon = (255, 160, 122)
Salmon = (250, 128, 114)
SoftBlush =(255, 228, 225)

# -------------------------
# CONFIG
# -------------------------
WIDTH = HEIGHT = 512
#400 is another option for the size of the chess board.
DIMENSION = 8
#Dimensions of Chess board is 8*8
SQ_SIZE = HEIGHT // DIMENSION
#square size is the height or width of the chess board divided by 8.
MAX_FPS = 60
#for Animations later on.

IMAGES = {}

# -------------------------
# LOAD PIECE IMAGES
# -------------------------
def loadImages():
    pieces = ["wp","wR","wN","wB","wQ","wK",
              "bp","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"),
            (SQ_SIZE, SQ_SIZE)
        )

# -------------------------
# MAIN
# -------------------------
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()

    moveMade = False
    checkmateAnimation = False
    animationFrame = 0

    loadImages()

    sqSelected = ()
    playerClicks = []

    running = True
    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            # -------------------------
            # MOUSE CLICK
            # -------------------------
            elif e.type == p.MOUSEBUTTONDOWN and not checkmateAnimation:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    if len(playerClicks) == 0:
                        if gs.board[row][col] != "--":
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board
                    )

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # -------------------------
            # KEY CONTROLS
            # -------------------------
            elif e.type == p.KEYDOWN:

                # UNDO (Z)
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    checkmateAnimation = False
                    animationFrame = 0

                # RESTART (R)
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    checkmateAnimation = False
                    animationFrame = 0

        # -------------------------
        # UPDATE MOVES
        # -------------------------
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        # -------------------------
        # TRIGGER CHECKMATE ANIMATION
        # -------------------------
        if gs.checkMate and not checkmateAnimation:
            checkmateAnimation = True
            animationFrame = 0

        # -------------------------
        # DRAW GAME
        # -------------------------
        drawGameState(screen, gs, sqSelected, validMoves)

        # -------------------------
        # CHECKMATE ANIMATION
        # -------------------------
        if checkmateAnimation:
            drawCheckmateAnimation(screen, gs, animationFrame)
            animationFrame += 1

        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()

# -------------------------
# CHECKMATE ANIMATION
# -------------------------
def drawCheckmateAnimation(screen, gs, frame):

    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(min(220, frame * 3))
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Highlight losing king
    color = "w" if gs.whiteToMove else "b"
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] == color + "K":
                glow = p.Surface((SQ_SIZE, SQ_SIZE))
                glow.set_alpha(180)
                glow.fill((200, 0, 0))
                screen.blit(glow, (c * SQ_SIZE, r * SQ_SIZE))

    size = min(80, 20 + frame * 2)
    font = p.font.SysFont("Arial", size, True)
    text = font.render("CHECKMATE", True, (255, 255, 255))
    textRect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, textRect)

    smallFont = p.font.SysFont("Arial", 28)
    restartText = smallFont.render("Press R to Restart", True, (255, 215, 0))
    restartRect = restartText.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restartText, restartRect)

# -------------------------
# DRAW BOARD & PIECES
# -------------------------
def drawGameState(screen, gs, sqSelected, validMoves):
    drawBoard(screen)

    if gs.inCheck():
        highlightKing(screen, gs)

    highlightSquares(screen, gs, sqSelected, validMoves)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color,
                        p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],
                            p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# -------------------------
# HIGHLIGHTS
# -------------------------
def highlightKing(screen, gs):
    color = "w" if gs.whiteToMove else "b"
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] == color + "K":
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(120)
                s.fill((255, 0, 0))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

def highlightSquares(screen, gs, sqSelected, validMoves):
    if sqSelected != ():
        r, c = sqSelected

        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill((255, 229, 180))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)

                if gs.board[move.endRow][move.endCol] != "--":
                    s.fill((255, 0, 0))
                else:
                    s.fill((0, 200, 0))

                screen.blit(s,
                            (move.endCol * SQ_SIZE,
                             move.endRow * SQ_SIZE))

if __name__ == "__main__":
    main()
