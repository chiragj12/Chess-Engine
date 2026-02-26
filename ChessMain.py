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


p.init()
WIDTH=HEIGHT=512
#400 is another option for the size of the chess board.
DIMENSION=8
#Dimensions of Chess board is 8*8
SQ_SIZE=HEIGHT//DIMENSION
#square size is the height or width of the chess board divided by 8.

MAX_FPS=15
#For animations.

IMAGES={}


def loadImages():
    pieces=["wp","wR","wN","wB","wQ","wK","bp","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    #Note :We can access an image by saying IMAGES["wp"]


    """The main driver for our code. This will handle user input and updating the graphics."""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()

    sqSelected = ()
    playerClicks = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []

                else:
        # FIRST CLICK → must be a real piece
                    if len(playerClicks) == 0:
                        if gs.board[row][col] != "--":
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

        # SECOND CLICK
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

    # Only create move if we have 2 VALID squares
                if len(playerClicks) == 2:
                    startSq = playerClicks[0]
                    endSq = playerClicks[1]

                    if startSq != () and endSq != ():
                        move = ChessEngine.Move(startSq, endSq, gs.board)

                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
                           
                    else:
                        playerClicks = []

                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    sqSelected = ()
                    playerClicks = []



    # update valid moves AFTER move
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

    # ALWAYS draw
        drawGameState(screen, gs, sqSelected, validMoves)

        if gs.checkMate:
            drawText(screen, "Black wins by Checkmate" if gs.whiteToMove else "White wins by Checkmate")

        elif gs.staleMate:
            drawText(screen, "Stalemate")

        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()





def drawGameState(screen, gs, sqSelected, validMoves):
    drawBoard(screen)
    highlightSquares(screen, gs, sqSelected, validMoves)
    drawPieces(screen, gs.board)
    





def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def highlightSquares(screen, gs, sqSelected, validMoves):
    if sqSelected != ():
        r, c = sqSelected

        # Highlight selected square (yellow)
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color(Peach))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

        # Highlight legal moves (green)
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)

                if gs.board[move.endRow][move.endCol] != "--":
                    s.fill(p.Color("red"))
                else:
                    s.fill(p.Color("green"))

                screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, False, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - textObject.get_width()/2,
        HEIGHT/2 - textObject.get_height()/2
    )
    screen.blit(textObject, textLocation)






if __name__ == "__main__":    
   main()

