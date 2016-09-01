import random
import copy
from time import time
import multiprocessing as mp
import dispy
class play:
	maxPlayer = 1
	minPlayer = -1
	def printGrid(self,grid):
		for i in range (0,3):
			row = i*3
			print(grid[row]," ",grid[row+1]," ",grid[row+2])

	def isEmpty(self,grid):
		for slot in range (0,9):
			if grid[slot] == 0:
				return True
		return False

	def isWinner(self,grid):
		combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
		(2, 5, 8), (0, 4, 8), (2, 4, 6))

		for t in combi:
			triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
			if triad_sum == 3 or triad_sum == -3:
				return grid[t[0]]
		return 0

	def isLeaf(self,grid):
		for slot in range (0,9):
			if grid[slot] == 0:
				return False
		return True

	def isWinner(self,grid):
		combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
		(2, 5, 8), (0, 4, 8), (2, 4, 6))

		for t in combi:
			triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
			if triad_sum == 3 or triad_sum == -3:
				return grid[t[0]]
		return 0

	def isWinnerMin(self,grid):
		combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
		(2, 5, 8), (0, 4, 8), (2, 4, 6))

		for t in combi:
			triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
			if triad_sum == -3:
				return 1
		return 0

	def isWinnerMax(self,grid):
		combi = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
		(2, 5, 8), (0, 4, 8), (2, 4, 6))

		for t in combi:
			triad_sum = grid[t[0]] + grid[t[1]] + grid[t[2]]
			if triad_sum == 3:
				return 1
		return 0

	def getChildren(self,grid,curPlayer):
		validMoves = []
		for move in range (0,9):
			if grid[move] == 0:
				grid[move] = curPlayer
				newMove = copy.deepcopy(grid)
				validMoves.append(newMove)
				grid[move] = 0
		return validMoves

	def getCost(self,node):
		nodeCost = 20
		if self.isWinnerMax(node) == True:
			nodeCost = 30
		elif self.isWinnerMin(node) == True:
			nodeCost = 10
		return nodeCost

	def TestSerial(self,grid,player,v,relation):
		if self.isLeaf(grid):
			val = self.getCost(grid)
			if relation == '>':
				res = (val > v)
			elif relation == '>=':
				res = (val >= v)
			if res == True:
				return True
			else:
				return False
		p = self.getChildren(grid,player)

		if player == self.maxPlayer:
			for i in range(0,len(p)):
				if self.TestSerial(p[i],self.minPlayer,v,relation) == True:
					return True
		elif player == self.minPlayer:
			for i in range(0,len(p)):
				if self.TestSerial(p[i],self.maxPlayer,v,relation) ==  False:
					return False
		if player == self.maxPlayer:
			return False
		else:
			return True
		return True

	def Test(self,grid,player,v,relation):#,output):
		if isLeaf(grid):
			val = self.getCost(grid)
			if relation == '>':
				res = (val > v)
			elif relation == '>=':
				res = (val >= v)
			if res == True:
				t = (grid,True)
				#output.put(t)
				return True
			else:
				t = (grid,False)
				#output.put(t)
				return False
		p = getChildren(grid,player)

		if player == self.maxPlayer:
			for i in range(0,len(p)):
				if TestSerial(p[i],self.minPlayer,v,relation) == True:
					t = (p[i],True)
					#output.put(t)
					return True
		elif player == self.minPlayer:
			for i in range(0,len(p)):
				if TestSerial(p[i],self.maxPlayer,v,relation) ==  False:
					t = (p[i],False)
					#output.put(t)
					return False
		if player == self.maxPlayer:
			t = (grid,False)
			#output.put(t)
			return False
		else:
			t = (grid,True)
			#output.put(t)
			return True
		return True

	def scout(self,grid,player):
		#print player
		validMoves =[]
		if self.isLeaf(grid):
			#print "here",self.getCost(grid),grid
			return self.getCost(grid),grid
		children = self.getChildren(grid,player)
		otherPlayer = self.maxPlayer
		if player == self.maxPlayer:
			otherPlayer = self.minPlayer
		s = children[0]
		v,mvs = self.scout(s,otherPlayer)
		best = v
		validMoves = [s]
		values = [v]
		if player == self.maxPlayer:
			for i in range(1,len(children)):
				if self.TestSerial(children[i],self.minPlayer,v,'>') == True:
					v,mvs = self.scout(children[i],self.minPlayer)
					values.append(v)
					if v > best:
						best = v
						validMoves = [children[i]]
					elif v >= best:
						validMoves.append(children[i])

			# print("Values are : ",values)
		elif player == self.minPlayer:
			for i in range(1,len(children)):
				if self.TestSerial(children[i],self.maxPlayer,v,'>=') == False:
					v,mvs =self.scout(children[i],self.maxPlayer)
					if v < best:
						best = v
						validMoves = [children[i]]
					elif v <= best:
						validMoves.append(children[i])
		return v,grid


