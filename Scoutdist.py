import random
import copy
from time import time
import multiprocessing as mp
import dispy
#output = mp.Queue()
from play import play
def scoutParallel(playObj,grid,player):#,output):
	validMoves =[]
	if playObj.isLeaf(grid):
		t = (grid,playObj.getCost(grid),validMoves)
		#output.put(t)
		return playObj.getCost(grid),grid
	children = playObj.getChildren(grid,player)
	otherPlayer = playObj.maxPlayer
	if player == playObj.maxPlayer:
		otherPlayer = playObj.minPlayer
	s = children[0]
	v,mvs = playObj.scout(s,otherPlayer)
	best = v
	validMoves = [s]
	values = [v]
	if player == playObj.maxPlayer:
		for i in range(1,len(children)):
			if seplayObjlf.TestSerial(children[i],playObj.minPlayer,v,'>') == True:
				v,mvs = playObj.scout(children[i],playObj.minPlayer)
				values.append(v)
				if v > best:
					best = v
					validMoves = [children[i]]
				elif v >= best:
					validMoves.append(children[i])

		# print("Values are : ",values)
	elif player == playObj.minPlayer:
		for i in range(1,len(children)):
			if playObj.TestSerial(children[i],playObj.maxPlayer,v,'>=') == False:
				v,mvs = playObj.scout(children[i],playObj.maxPlayer)
				if v < best:
					best = v
					validMoves = [children[i]]
				elif v <= best:
					validMoves.append(children[i])
	t = (grid,v,validMoves)
	#output.put(t)
	return v,grid

def search(playObj,grid,player):
	validMoves =[]
	if playObj.isLeaf(grid):
		return playObj.getCost(grid),validMoves
	children = playObj.getChildren(grid,player)
	otherPlayer = playObj.maxPlayer
	if player == playObj.maxPlayer:
		otherPlayer = playObj.minPlayer
	s = children[0]
	v,mvs = playObj.scout(s,otherPlayer)
	best = v
	validMoves = [s]
	values = [v]
	cluster = dispy.JobCluster(scoutParallel,depends=[])
	if player == playObj.maxPlayer:
		validChildren = [children[0]]
		for i in range(1,len(children)):
			if playObj.TestSerial(children[i],playObj.minPlayer,v,'>') == True:
				validChildren.append(children[i])
		jobs=[]
		for i in range(0,len(validChildren)):
			job= cluster.submit(playObj,children[i],playObj.minPlayer)
			job.id=i
			jobs.append(job)


		results=[]
		for job in jobs:
	
			returnedbyProc =  job() # waits for job to finish and returns results
			if(results is None):
				print job.exception
			else:
				print "STDOUT",job.stdout , job.exception
			
			results.append(returnedbyProc)
		#processes =[cluster.submit(children[i],self.minPlayer)  for i in range(0, len(self.validChildren))] #[mp.Process(target=self.scoutParallel, args=(children[i], self.minPlayer)) for i in range(0, len(self.validChildren))]
		# Run processes
		
		'''for p in processes:
			p.start()

		for p in processes:
			p.join()

		# Get process results from the output queue
		#results = [output.get() for p in processes]
		'''
		print"results ",(results)
		print (len(results))
		for v,mvs in results:
			print v,mvs
			if v > best:
				best = v
				validMoves = mvs
			elif v >= best:
				validMoves.append(mvs)
		cluster.print_status()
		'''for cnt in range(0,len(results)):
			v = results[cnt][1]

			mvs = results[cnt][2]
			if v > best:
				best = v
				validMoves = [results[cnt][0]]
			elif v >= best:
				validMoves.append(results[cnt][0])'''
	print "V",v
	print "G",grid
	return v,validMoves 	


turn = 1# player will play
playObj = play()
grid = []
for i in range (0,9):
	grid.append(0)
'''grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
grid = [1, 0, 0, 0, 0, 0, 0, 0, -1]
grid = [1, 1, -1, 0, 0, 0, 0, 0,-1]
grid = [0, 0, 0, 0, -1, 0, 0, 0, 0]
grid = [0, 0, 1, 0, -1, 0, -1, 0, 0]
grid = [-1, 0, 1, 0, -1, 0, -1, 0, 0]
grid = [1, 0, 0, 0, -1, 0, 0, 0, -1]
grid = [1, 0, -1, 0, -1, 0, 0, 1, -1]
grid = [0, 0, 0, 0, -1, 1, 0, 0, -1]
grid = [0, -1, 0, 0, 0, 0, 0, 0, 0]'''
while playObj.isEmpty(grid) and playObj.isWinner(grid) == 0:
	print('Current Grid : ')
	playObj.printGrid(grid)

	if turn == 1 and playObj.isEmpty(grid):
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
		if playObj.isWinnerMin(grid) :
			break
		playObj.printGrid(grid)
		turn = 0

	if turn == 0 and playObj.isEmpty(grid):
		start = time()
		# val,mymvs = scout(grid,self.maxPlayer)
		val,mymvs = search(playObj,grid,playObj.maxPlayer)
		print("got best as : ",val)
		print("moves : ",mymvs)
		mymv = random.choice(mymvs)
		print("I choose", mymv)
		grid = mymv
		turn = 1
		finish = time()
		print("Time taken : ",finish -start)

playObj.printGrid(grid)
res = playObj.isWinner(grid)
if res == -1:
	print("You won...")
elif res == 1:
	print("Computer won...")
else:
	print("Draw")

