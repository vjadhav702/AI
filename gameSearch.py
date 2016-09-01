

debug = False
inf = float('infinity')

def negamax(game, depthLeft,alpha,beta):
    if debug: print '   '*(10-depthLeft), game,

    if game.checkGameExists() :
        if debug: print 'terminal value',game.getStatus()
        return game.getStatus(), None
    if debug: print

    bestValue = -inf
    bestMove = None
    for move in game.getNextMovement():

        game.changeGAMEBOARDbyMove(move)

        value = - negamax(game,depthLeft-1,-beta,-alpha)[0]

        game.unchangeGAMEBOARDbyMove(move)
        if debug: print '   '*(10-depthLeft), game, "move",move,"backed up value",value,
        if value > bestValue:

            bestValue = value
            bestMove = move
            if debug: print "new best"
        else:
            if debug: print
	if(bestValue>=beta):
		break
	alpha = max([alpha,bestValue])
	
    return bestValue, bestMove
