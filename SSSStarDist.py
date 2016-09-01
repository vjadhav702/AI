import sys
import heapq
import numpy as np
import random
import re
import dispy
from time import time
import multiprocessing as mp

from random import randint
import copy
from GameNodeFile import GameNode       
sys.path.append('/home/vinayak/Desktop/AI/vinayak_Distributed/')
output = []#mp.Queue()

whoseTurn = 0

listOne = []
listZero = []
listMinusOne = []

MARKERS = ['_', 'O', 'X']
myBoard = [0,0,0,0,0,0,0,0,0]


def processNodes(newnode) :
    
    MAXVALUE = 5000
    LIVE = "LIVE"
    SOLVED = "SOLVED"
    MAXNODE = "MAX"
    MINNODE = "MIN"
    LEAF = "LEAF"
    BOARDSIZE = 9

    openList = []


    currentBoard = copy.deepcopy(newnode.board)
    #global MINNODE
    newnode.type = MINNODE
    newnode.isRoot = "Y"
    newnode.isExamined = "Y"

    newnode.addDetails(newnode)

    heapq.heappush(openList,newnode)

    dataVal = newnode.SSSStar(openList)
    #myBoard = copy.deepcopy(tempMyBoard)

    dictResult = {}
    dictResult[dataVal] = currentBoard
    

    global whoseTurn
    whoseTurn = 0
    
    return dictResult

####################### start main here ############################
if True:

    temp = GameNode()
    while(temp.isWinner(myBoard) == 0):#do this while any one of them will win

        if whoseTurn == 0 :#humans turn

            choice = temp.recv_human_move(myBoard)
            myBoard[choice] = -1
            whoseTurn = 1

            listOne = []
            listZero = []
            listMinusOne = []

        else:#computer turn

            jobs = []
            cluster = dispy.JobCluster(processNodes,depends=[])
            print("Waiting for system to find its move ........")

            #processes = []

            for i in range(0, 9):
                if myBoard[i] == 0:

                    newnode = GameNode()
                    newnode.board = copy.deepcopy(myBoard)

                    newnode.board[i] = 1
                    #tempProcess = mp.Process(target=processNodes, args=(newnode, output))
                    #processes.append(tempProcess)
                    job = cluster.submit(newnode)
                    job.id = i # optionally associate an ID to job (if needed later)
                    jobs.append(job)
            #print " number of jobs ",len(jobs)
            start = time()


            finish = time()
            cluster.wait()
            for p in jobs:

                dictData = p()
                      
                print(dictData)
                myDict = dictData
               # print(  "dict0",myDict.keys())
                print("stdout",p.stdout)
                print("except",p.exception)
        
                if 1 in myDict.keys():
                    listOne.append(myDict[1])
                elif 0 in myDict.keys():
                    listZero.append(myDict[0])
                else :
                    listMinusOne.append(myDict[-1])
                
            if len(listOne) > 0:

                myBoard = copy.deepcopy(random.choice(listOne))
            elif len(listZero) > 0:

                myBoard = copy.deepcopy(random.choice(listZero))
            elif len(listMinusOne) > 0:

                myBoard = copy.deepcopy(random.choice(listMinusOne))
            cluster.print_status()

            #print("============================ After comp turn ============================= ", myBoard)
            j = 0
            print("Current status of the board ")
            temp = GameNode()
            for i in range (0, 3):
            
                print(temp.MARKERS[myBoard[j]],"|",temp.MARKERS[myBoard[j+1]],"|",temp.MARKERS[myBoard[j+2]])
                j += 3
            
            print('\n')
            print("Time taken : ",finish-start)
            whoseTurn = 0

    #print(END_PHRASE[isWinner(myBoard)])
    finalDat = temp.isWinner(myBoard)
    if finalDat == 10:
        finalDat = 0
    print(["Tie", "Computer Won", "You won"][finalDat])
