
import numpy as np

class GomokuGame:
    SEGLENGTH = 3
    CHAR_1 = 'X'
    CHAR_2 = '0'

    def __init__(self, gameNo, tblRows, tblCols):
        self.tblRows = tblRows
        self.tblCols = tblCols
        self.table = np.ndarray((tblRows, tblCols), dtype=np.int8)
        #self.table[:] = ' '
        self.gameNo = gameNo

    def printTable(self):
        print(np.array2string(self.table, formatter={'str':lambda x: 'X' if x==1 else '0' if x==2 else ' '}, separator = ' '))
        #print (self.table)

    def checkWinnerRows(self, tbl):
        ar = tbl
        print(ar.flatten())


    def checkWinner (self):
        # check rows
        self.checkWinnerRows(self.table)
        # check columns
        self.checkWinnerRows(np.transpose(self.table))


    def makeMove(self, r, c):
        self.table[r-1][c-1] = 1


class GameSimulator:
    def __init__(self, nrOfGames):
        self.nrOfGames = nrOfGames

    def simulate(self):
        for g in range(self.nrOfGames):
            game = GomokuGame(g, 3, 4)
            game.makeMove(3,3)
            game.makeMove(1, 2)
            game.makeMove(1, 1)
            game.makeMove(2, 2)
            

game = GomokuGame(1, 3, 4)
game.makeMove(1, 2)
game.makeMove(1, 1)
game.makeMove(2, 2)
game.checkWinner()

game.printTable()