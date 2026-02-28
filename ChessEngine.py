class GameState:
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkMate = False
        self.staleMate = False

        self.moveLog = []

        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }

    # -------------------------
    # MAKE / UNDO MOVE
    # -------------------------
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            self.whiteToMove = not self.whiteToMove

    # -------------------------
    # CHECK DETECTION
    # -------------------------
    def inCheck(self):
        if self.whiteToMove:
            row, col = self.whiteKingLocation
        else:
            row, col = self.blackKingLocation
        return self.squareUnderAttack(row, col)

    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove

        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

    # -------------------------
    # VALID MOVES
    # -------------------------
    def getValidMoves(self):
        self.checkMate = False
        self.staleMate = False

        moves = self.getAllPossibleMoves()
        validMoves = []

        for move in moves:
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove

            if not self.inCheck():
                validMoves.append(move)

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(validMoves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        return validMoves

    # -------------------------
    # GENERATE ALL MOVES
    # -------------------------
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "--":
                    continue

                turn = piece[0]
                if (turn == 'w' and self.whiteToMove) or \
                   (turn == 'b' and not self.whiteToMove):

                    pieceType = piece[1]
                    self.moveFunctions[pieceType](r, c, moves)

        return moves

    # -------------------------
    # PAWN
    # -------------------------
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r-1 >= 0 and self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))

            if r-1 >= 0 and c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if r-1 >= 0 and c+1 <= 7 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if r+1 <= 7 and self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))

            if r+1 <= 7 and c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if r+1 <= 7 and c+1 <= 7 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r,c),(r+1,c+1),self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2,-1),(-2,1),(-1,-2),(-1,2),
                       (1,-2),(1,2),(2,-1),(2,1)]
        allyColor = 'w' if self.whiteToMove else 'b'

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = [(-1,-1),(-1,0),(-1,1),
                     (0,-1),(0,1),
                     (1,-1),(1,0),(1,1)]
        allyColor = 'w' if self.whiteToMove else 'b'

        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


class Move:
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.startRow == other.startRow and
                    self.startCol == other.startCol and
                    self.endRow == other.endRow and
                    self.endCol == other.endCol)
        return False
