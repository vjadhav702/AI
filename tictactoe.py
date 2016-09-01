class tictactoe:

    def __init__(self,debug=False):
        self.debug = debug
        self.GAMEBOARD =  [' ']*9
        self.player = 'X'
        if False:
            self.GAMEBOARD = ['X','X',' ', 'X','O','O',' ',' ',' ']
            self.player = 'O'
        self.nxPlayer = self.player

    def locations(self,c):
        return filter(lambda i: self.GAMEBOARD[i] == c, range(len(self.GAMEBOARD)))

    def getNextMovement(self):
        moves = self.locations(' ')
	#print "moves",moves
        return moves
        
    def getStatus(self):
        currentX = self.locations('X')
        currentO = self.locations('O')
        wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
        xWINCHECK = any([all([wi in currentX for wi in w]) for w in wins])
        OWINCHECK = any([all([wi in currentO for wi in w]) for w in wins])
        if xWINCHECK:
            return 1 if self.nxPlayer is 'X' else -1
        elif OWINCHECK:
            return 1 if self.nxPlayer is 'O' else -1
        elif ' ' not in self.GAMEBOARD:
            return 0
        else:
            return None
            
    def checkGameExists(self):
        return self.getStatus() != None

    def changeGAMEBOARDbyMove(self,move):
        self.GAMEBOARD[move] = self.nxPlayer
        self.nxPlayer = 'X' if self.nxPlayer=='O' else 'O'

    def turnChange(self):
        self.player = 'X' if self.player=='O' else 'O'
        self.nxPlayer = self.player

    def unchangeGAMEBOARDbyMove(self,move):
        self.GAMEBOARD[move] = ' '
        self.nxPlayer = 'X' if self.nxPlayer=='O' else 'O'

    def __str__(self):
        if self.debug:
            s = "|%c%c%c|%c%c%c|%c%c%c|" % tuple(self.GAMEBOARD)
        else:
            s = "%c|%c|%c\n-----\n%c|%c|%c\n-----\n%c|%c|%c" % tuple(self.GAMEBOARD)
        return s
