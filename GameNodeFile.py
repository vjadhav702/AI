import sys
import numpy as np
import random
import re
from time import time
import multiprocessing as mp
import heapq 
from random import randint
import copy

class GameNode:

    MAXVALUE = 5000
    LIVE = "LIVE"
    SOLVED = "SOLVED"
    MAXNODE = "MAX"
    MINNODE = "MIN"
    LEAF = "LEAF"
    BOARDSIZE = 9

    WINNING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))
    PRINTING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
    MARKERS = ['_', 'O', 'X']

    board = []
    listChild = []
    type = ""
    status = ""
    eValue = 0
    isRoot = ""
    isExamined = ""
    parent = None

    def __init__(self):
        self.board = np.zeros((self.BOARDSIZE), dtype=int)
        self.listChild = []
        self.status = self.LIVE
        self.type = ""
        self.eValue = self.MAXVALUE
        self.isRoot = "N"
        self.isExamined = "N"


    def __lt__(self, other):
        return (self.eValue >= other.eValue)

    def addDetails(self, node):

        for i in range(0,self.BOARDSIZE):
            if node.board[i] == 0:
                tempNode = GameNode()

                if node.type == self.MAXNODE :
                    tempNode.type = self.MINNODE
                else:
                    tempNode.type = self.MAXNODE

                for j in range(0, self.BOARDSIZE):
                    tempNode.board[j] = node.board[j]

                #tempNode.board = copy.deepcopy(node.board)
                if node.type == self.MAXNODE:
                    tempNode.board[i] =  1
                else :
                    tempNode.board[i] =  -1

                #tempNode.board[i] =  1
                tempNode.parent = node

                tempStatus = node.checkIsLeaf(tempNode)

                if tempStatus == 'Y':
                    tempNode.type = self.LEAF
                    tempVal = node.evaluateLeafNode(tempNode)
                    tempNode.eValue = tempVal

                listChild = node.listChild
                listChild.append(tempNode)
                node.listChild = listChild

                if tempStatus == 'N':
                    node.addDetails(tempNode)

        return


    def evaluateLeafNode(self, node):

        for triad in self.WINNING_TRIADS:
            triad_sum = node.board[triad[0]] + node.board[triad[1]] + node.board[triad[2]]
            if triad_sum == 3 or triad_sum == -3:
                #print("Value ======================",node.board[triad[0]])
                 return node.board[triad[0]]  # Take advantage of "_token" values
        return 0

    def checkIsLeaf(self, node):

        count = 0
        for i in range(0, self.BOARDSIZE):
            if node.board[i] == 0:
                count += 1
                #if count > 1:
                    #return "N"

        if count == 0:
            return "Y"
        else :
            return "N"

    def removeParentNode(self, node, openList):

        if openList.count(node) != 0:
            openList.remove(node)

        return

    def minVal(self, a, b):

        if a < b:
            return a
        else:
            return b

    def isWinner(self, tempBord):

         count = 0
         for triad in self.WINNING_TRIADS:
            triad_sum = tempBord[triad[0]] + tempBord[triad[1]] + tempBord[triad[2]]
            if triad_sum == 3 or triad_sum == -3:
                #print("Value ======================",node.board[triad[0]])
                 return tempBord[triad[0]]  #Take advantage of "_token" values

         for i in range(0, self.BOARDSIZE):
             if tempBord[i] == 0:
                 return 0

         return 10


    def SSSStar(self, openList):
        temp = GameNode()
        while True :

            #print("Before printing" ,len(openList))
            current = heapq.heappop(openList)
            #print(current.type, current.board, current.status, current.eValue)
            #print(len(openList))

            if current.status == self.LIVE:
                if current.type == self.LEAF:

                    parent = current.parent

                    if parent.type == self.MAXNODE:
                        current.type = self.MINNODE
                    else :
                        current.type = self.MAXNODE

                    current.status = self.SOLVED
                    val = temp.evaluateLeafNode(current)
                    current.eValue = val
                    heapq.heappush(openList,current)

                elif current.type == self.MINNODE:
                    allChilds = current.listChild
                    if len(allChilds) > 0:
                        childNode = allChilds[0]
                        childNode.isExamed = "Y"
                        heapq.heappush(openList,childNode)

                elif current.type == self.MAXNODE:
                    allChilds = current.listChild

                    for i in range(0, len(allChilds)):
                        childNode = allChilds[i]
                        childNode.isExamed = "Y"
                        heapq.heappush(openList,childNode)

            elif current.status == self.SOLVED:

                if current.isRoot == "Y":
                    return current.eValue

                elif current.type == self.MINNODE:
                    myParent = current.parent
                    temp.removeParentNode(myParent, openList)

                    myParent.status = self.SOLVED
                    myParent.isExamined = "Y"
                    #myParent.eValue = current.eValue
                    myParent.eValue = temp.minVal(myParent.eValue, current.eValue)
                    if myParent.isRoot == "Y":
                        myParent.board = copy.deepcopy(current.board)
                    heapq.heappush(openList, myParent)

                elif current.type == self.MAXNODE:

                    tempFlag = False
                    allChilds = current.parent.listChild
                    for i in range(0, len(allChilds)):

                        tempChild = allChilds[i]

                        if current is tempChild :#I should not be that child
                            continue

                        if tempChild.isExamined == "N":
                            #print("child to be added is ", tempChild.board)
                            tempChild.isExamined = "Y"
                            #tempChild.eValue = current.eValue
                            tempChild.eValue = temp.minVal(current.eValue, tempChild.eValue)
                            #tempChild.type = self.MAXNODE
                            tempFlag = True
                            heapq.heappush(openList, tempChild)
                            break

                    if not tempFlag :
                        myP = current.parent
                        myP.status = self.SOLVED
                        myP.isExamined = "Y"
                        #myP.eValue = current.eValue
                        myP.eValue = temp.minVal(current.eValue, myP.eValue)

                        if myP.isRoot == "Y":
                            myP.board = copy.deepcopy(current.board)

                        heapq.heappush(openList, myP)

        return

    def print_board(self, board):
        
        temp = GameNode()
        '''for row in self.PRINTING_TRIADS:
            for hole in row:
                print(self.MARKERS[board[hole]])
            print()'''
        print("Current status of the board ")
        j = 0
        for i in range (0, 3):
            
            print(temp.MARKERS[board[j]],"|",temp.MARKERS[board[j+1]],"|",temp.MARKERS[board[j+2]])
            j += 3
            
        print('\n')

    def recv_human_move(self, board):
        
        looping = True
        while looping:
            try:
                inp = input("Your move: ")
                yrmv = int(inp)
                if 0 <= yrmv <= 8:
                    if board[yrmv] == 0:
                        looping = False
                    else:
                        print("Spot already filled.")
                else:
                    print("Bad move.")

            except EOFError:
                print('\n')
                sys.exit(0)
            except NameError:
                print("Not 0-9, try again.")
            except SyntaxError:
                print("Not 0-9, try again.")

            if looping:
                GameNode().print_board(board)

        return yrmv
