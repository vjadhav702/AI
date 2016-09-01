import gameSearch as gs
import tictactoe
from time 	import time
debug = False

def playGameNegamax(game):
    print game
    while not game.checkGameExists():
	if(game.player=='X'):
		userInput = input("Enter move: ")
		userMove = int(userInput)
		if(userMove <0 or userMove > 8 or not (game.GAMEBOARD[userMove] ==' ')):
			continue
		game.changeGAMEBOARDbyMove(userMove)
		game.turnChange()
	else:
		start = time()
		value,move = gs.negamax(game,9,-200,200)
		if move == None :
		    print "move is None. Stopping"
		    break
		game.changeGAMEBOARDbyMove(move)
		print "Player",game.player,"to",move,"for value",value,
		if not debug: print
		print game
		finish = time()
		game.turnChange()
		print("Time:" , finish - start)

gameObj =tictactoe.tictactoe(debug)
print gameObj.player
#gameObj.turnChange()
#print gameObj.player
playGameNegamax(gameObj)
