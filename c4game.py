class C4State:
    
    #constants for game result
    NOT_COMPLETE = 0
    P1_WON = 1
    P2_WON = 2
    TIE = 3

    @staticmethod
    def generateBoard(rows, cols):
        return [[0 for j in range(cols)] for i in range(rows)]
    
    def clone(self):
        cloned = C4State(self.rows, self.cols, self.connect)
        cloned.currentPlayer = self.currentPlayer
        cloned.moveCounter = self.moveCounter
        cloned.result = self.result
        for i in range(self.rows):
            for j in range(self.cols):
                cloned.board[i][j] = self.board[i][j]
        return cloned

    def __init__(self, rows=6, cols=7, connect=4):
        self.rows = rows
        self.cols = cols
        self.connect = connect
        self.board = C4State.generateBoard(self.rows, self.cols)
        self.currentPlayer = 1
        self.moveCounter = 0
        self.maxMoves = self.rows*self.cols
        self.result = C4State.NOT_COMPLETE

class C4Game:

    def __init__(self, state=C4State()):
        self._state = state

    def getState(self):
        return self._state.clone()

    def move(self, player, col):
        #some validations
        if self._state.result != C4State.NOT_COMPLETE:
            raise C4Exception('Game is complete, cant do move')
        if self._state.currentPlayer != player:
            raise C4Exception('current player does not match')
        if col < 0 or col > (self._state.cols - 1):
            raise C4Exception('col out of bound')
        if self._isColFull(col):
            raise C4Exception('col is full')
        
        #putting token
        for i in range(self._state.rows-1, -1, -1):
            if self._state.board[i][col] == 0:
                self._state.board[i][col] = player
                break
        
        #at this moment i contains row in which token placed
        if self._isGameComplete(i, col):
            if self._state.maxMoves-1 <= self._state.moveCounter:
                self._state.result = C4State.TIE
            elif player == 1:
                self._state.result = C4State.P1_WON
            else:
                self._state.result = C4State.P2_WON
            return self.getState()

        self._state.moveCounter = self._state.moveCounter + 1
        self._state.currentPlayer = self._state.moveCounter % 2 + 1
        return self.getState()

    def _isGameComplete(self, row, col):
        connect = self._state.connect - 1
        if (self._getCoinsCountInDir(row, col, 1) +  self._getCoinsCountInDir(row, col, 5) >= connect):
            return True
        if (self._getCoinsCountInDir(row, col, 2) +  self._getCoinsCountInDir(row, col, 6) >= connect):
            return True
        if (self._getCoinsCountInDir(row, col, 3) +  self._getCoinsCountInDir(row, col, 7) >= connect):
            return True
        if (self._getCoinsCountInDir(row, col, 4) +  self._getCoinsCountInDir(row, col, 8) >= connect):
            return True
        if (self._state.moveCounter >= self._state.maxMoves-1):
            return True
        return False

    def _getCoinsCountInDir(self, r, c, dir):
        player = self._state.board[r][c]
        count = 0 
        dir -= 1 
        dirRow = [-1, -1, -1, 0, 1, 1, 1, 0] 
        dirCol = [-1, 0, 1, 1, 1, 0, -1, -1] 
        changeCol = dirCol[dir] 
        changeRow = dirRow[dir] 
        r += changeRow 
        c += changeCol 
        while (r >= 0 and r < self._state.rows and c >= 0 and c < self._state.cols):
            if player == self._state.board[r][c]:
                count = count + 1
                r += changeRow 
                c += changeCol 
            else:
                break 
        return count 
        
    def _isColFull(self, col):
        return self._state.board[0][col] != 0

class C4Exception(Exception):
    pass