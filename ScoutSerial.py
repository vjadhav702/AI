import random
import copy
from time import time
maxPlayer = 1
minPlayer = -1
MARKERS = ['-', 'O', 'X']

def printGrid(grid):
    for i in range (0,3):
        row = i*3
        print(MARKERS[grid[row]],"|",MARKERS[grid[row+1]],"|",MARKERS[grid[row+2]])

def isEmpty(grid):
    for slot in range (0,9):
        if grid[slot] == 0:
            return True
    return False

def isWinner(grid):
    combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))

    for t in combi:
        triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
        if triad_sum == 3 or triad_sum == -3:
            return grid[t[0]]
    return 0

def isLeaf(grid):
    for slot in range (0,9):
        if grid[slot] == 0:
            return False
    return True

def isWinner(grid):
    combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))

    for t in combi:
        triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
        if triad_sum == 3 or triad_sum == -3:
            return grid[t[0]]
    return 0

def isWinnerMin(grid):
    combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))

    for t in combi:
        triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
        if triad_sum == -3:
            return 1
    return 0

def isWinnerMax(grid):
    combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))

    for t in combi:
        triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
        if triad_sum == 3:
            return 1
    return 0

def getChildren(grid,curPlayer):
    validMoves = []
    for move in range (0,9):
        if grid[move] == 0:
            grid[move] = curPlayer
            newMove = copy.deepcopy(grid)
            validMoves.append(newMove)
            grid[move] = 0
    return validMoves

def getCost(node):
    nodeCost = 20
    if isWinnerMax(node) == True:
        nodeCost = 30
    elif isWinnerMin(node) == True:
        nodeCost = 10
    return nodeCost

def Test(grid,player,v,relation):

    if isLeaf(grid):
        val = getCost(grid)
        if relation == '>':
            res = (val > v)
        elif relation == '>=':
            res = (val >= v)
        if res == True:
            return True
        else:
            return False
    p = getChildren(grid,player)

    if player == maxPlayer:
        for i in range(0,len(p)):
            if Test(p[i],minPlayer,v,relation) == True:
                return True
    elif player == minPlayer:
        for i in range(0,len(p)):
            if Test(p[i],maxPlayer,v,relation) ==  False:
                return False
    if player == maxPlayer:
        return False
    else:
        return True
    return

def scout(grid,player):
    validMoves =[]
    if isLeaf(grid):
        return getCost(grid),validMoves
    children = getChildren(grid,player)
    otherPlayer = maxPlayer
    if player == maxPlayer:
        otherPlayer = minPlayer
    s = children[0]
    v,mvs = scout(s,otherPlayer)
    best = v
    validMoves = [s]
    values = [v]
    if player == maxPlayer:
        for i in range(1,len(children)):
            # if Test(children[i],minPlayer,v,'>') == True:
                v,mvs = scout(children[i],minPlayer)
                values.append(v)
                if v > best:
                    best = v
                    validMoves = [children[i]]
                elif v >= best:
                    validMoves.append(children[i])

        # print("Values are : ",values)
    elif player == minPlayer:
        for i in range(1,len(children)):
            # if Test(children[i],maxPlayer,v,'>=') == False:
                v,mvs = scout(children[i],maxPlayer)
                if v < best:
                    best = v
                    validMoves = [children[i]]
                elif v <= best:
                    validMoves.append(children[i])
    return v,validMoves

if __name__ == '__main__':
    turn = 1# player will play
    grid = []
    for i in range (0,9):
        grid.append(0)

    while isEmpty(grid) and isWinner(grid) == 0:
        print('Current Grid : ')
        printGrid(grid)

        if turn == 1 and isEmpty(grid):
            while 1:
                move = input("Enter move: ")
                moveInt = int(move)
                if 0 <= moveInt  <= 8:
                    if grid[moveInt ] == 0:
                        break
                    else:
                        print("Select empty tile..")
                else:
                    print("Select valid one..")

            grid[moveInt] = -1
            if isWinnerMin(grid) :
                break
            printGrid(grid)
            turn = 0

        if turn == 0 and isEmpty(grid):
            start = time()
            val,mymvs = scout(grid,maxPlayer)
            print("got best as : ",val)
            print("moves : ",mymvs)
            mymv = random.choice(mymvs)
            print("I choose", mymv)
            # # grid[mymv] = 1
            grid = mymv
            turn = 1
            finish = time()
            print("Time taken : ",finish -start)

    printGrid(grid)
    res = isWinner(grid)
    if res == -1:
        print("You won...")
    elif res == 1:
        print("Computer won...")
    else:
        print("Draw")


