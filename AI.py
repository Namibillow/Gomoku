import random


class FirstLevelNode:
    def __init__(self,data=1, row=0, column=0):
        self.connections = []
        self.AIData = data
        self.enemyData = 1
        self.row = row
        self.column = column

class SecondLevelNode:
    def __init__(self, connections):
        ### connections contains addresses of 5 indexs of matrix[row, col]
        self.connections = connections
        for firstLevelNode in self.connections:
            ### adding self to each addresses 
            firstLevelNode.connections.append(self)

    def getAIScore(self):
        output = 1
        numInARow = []
        numInARowCount = 0
        for firstLevelNode in self.connections:
            if firstLevelNode.AIData == 1.2:
                numInARowCount += 1
            numInARow.append(firstLevelNode)
            output *= firstLevelNode.AIData

        ### Open Three
        if numInARowCount == 3 and numInARow[0].AIData == 1 and numInARow[4].AIData == 1:
            return 5000
        ### Connect 4 
        if numInARowCount == 4:
            return 100000
        
        return output * numInARowCount

    def getEnemyScore(self):
        output = 1
        numInARow = []
        numInARowCount = 0
        for firstLevelNode in self.connections:
            if firstLevelNode.enemyData == 1.2:
                numInARowCount += 1
            numInARow.append(firstLevelNode)
            output *= firstLevelNode.enemyData

        ### Open three 
        ### Have higher score than getAIScore open three since AI needs to defense opponent
        if numInARowCount == 3 and numInARow[0].enemyData == 1 and numInARow[4].enemyData == 1:
            return 8000
        
        if numInARowCount == 4:
            return 10000
        # if numInARow == 0:
        #     return output
        return output * numInARowCount

class ThirdLevelNode:
    def __init__(self, connections):
        self.connections = connections

    def getAIScore(self):
        output = 0
        for secondLevelNode in self.connections:
            output += secondLevelNode.getAIScore()
        return output

    def getEnemyScore(self):
        output = 0
        for secondLevelNode in self.connections:
            output += secondLevelNode.getEnemyScore()
        return output

    def connect(self, secondLevelNode):
        self.connections.append(secondLevelNode)


class Space:
    def __init__(self, condition = 'e', row=0, column=0):
        self.row = row
        self.column = column
        self.condition = condition
        self.network = ThirdLevelNode([])
        self.node = FirstLevelNode(row = row, column = column)
        self.AIscore = 0
        self.enemyScore = 0
        self.totalScore = 0

    def updateScore(self):
        self.AIscore = self.network.getAIScore()
        self.enemyScore = self.network.getEnemyScore()
        self.totalScore = self.AIscore + self.enemyScore

    
class Board:
    def __init__(self):
        #e=empty, b=black, w=white
        #set 19x19 matrix with all spaces empty
        self.height = 19
        self.width = 19
        self.matrix = [[Space(condition = 'e', row=i,column=j) for i in range(self.height)]for j in range(self.width)]

        ### Contains all the possible winning combinations
        self.winningSetList = self.__calculateWinningSetList()
        self.generateNetworks()

    def __calculateWinningSetList(self):
        """
        It returns a list of list that contains the 5 tuples (connected five) 
        b = [[(row,col),(row2,col2),(row3,col3),(row4,col4)],[....],....]
        There is a total of 1020 possible win combinations.
        """
        b = []
        ### Horizontal
        for r in range(19):
            for c in range(15):
                b.append([(r, c), (r, c + 1), (r, c + 2), (r, c + 3), (r, c + 4)])

        ### Vertical
        for r in range(15):
            for c in range(19):
                b.append([(r, c), (r + 1, c), (r + 2, c), (r + 3, c), (r + 4, c)])

        ### Up
        for r in range(15):
            for c in range(15):
                b.append([(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3), (r + 4, c + 4)])

        ### Down
        for r in range(15):
            for c in range(4, 19):
                b.append([(r, c), (r + 1, c - 1), (r + 2, c - 2), (r + 3, c - 3), (r + 4, c - 4)])

        return b

    def generateNetworks(self):
        """
        Creates a tree kind of network where 
        - First Level 

        - Second Level contains 1020 nodes (# of the possible win combinations )
                       Each node points to 5 of the First Level nodes

        - Third Level contains 361 nodes (19 * 19)
        """
        secondLevelNodesList = []
        for winningSet in self.winningSetList:
            referenceToFirstLevelNodesList = []
            ### convert coords to list of firstLevelNodes
            for coordinate in winningSet:
                ### coordinate = (row,col)
                ### coordinate[0] = row, coordinate[1] = col
                referenceToFirstLevelNodesList.append(self.matrix[coordinate[0]][coordinate[1]].node)

            ### secondLevelNodesList contains the address of the secondLevel
            ### there should be 1020 
            secondLevelNodesList.append(SecondLevelNode(connections=referenceToFirstLevelNodesList))


        list = []
        #problem area. all top level connected to all second level
        for row in self.matrix:
            for space in row:
                for secondLevelNode in secondLevelNodesList:
                    if secondLevelNode.connections.__contains__(space.node):
                        space.network.connect(secondLevelNode)
                        ### Each [row,col] on the board contains secondLevelNode address
        
        # take each coordinate in a winning set and add the node containing that
        # index to the network of the space at that index
        self.updateAllScores()


    def printBoard(self):
        print()
        for row in self.matrix:
            for space in row:
                score = space.totalScore
                if score < 10:
                    print(score, end='  ')
                else:
                    print(score, end=' ')
            print()
        print()

        print()
        for row in self.matrix:
            for space in row:
                print(space.condition, end= ' ')
            print()
        print()

    def placeEnemy(self,row,column):
        space = self.matrix[row][column]
        space.condition = 'b'
        space.node.AIData = 0
        space.node.enemyData = 1.2
        self.updateAllScores()

    def placeSelf(self,row,column):
        space = self.matrix[row][column]
        space.condition = 'w'
        space.node.AIData = 1.2
        space.node.enemyData = 0
        self.updateAllScores()

    def updateAllScores(self):
        for row in self.matrix:
            for space in row:
                space.updateScore()

    def newBestMove(self):
        # trying to use already used spaces as bestMove
        # self.updateAllScores()
        # maxConditionList = []
        max = Space(row=-1, column=-1)
        for row in self.matrix:
            for space in row:
                if space.totalScore > max.totalScore and space.condition == 'e':
                    max = space
        maxList = []
        maxList.append(max)
        for row in self.matrix:
            for space in row:
                if space.totalScore == max.totalScore and space.condition == 'e':
                    maxList.append(space)
        max = maxList[random.randint(0, maxList.__len__() - 1)]
        # workaround
        return max.column, max.row

