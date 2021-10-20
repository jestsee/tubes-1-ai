import random
from time import time

from numpy.core.fromnumeric import shape
from src.model import board
from src.model import piece
from src.model.board import Board
from src.model.piece import Piece

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

import numpy as np
from copy import deepcopy

from src.utility import place

class LocalSearchGroup37:
    def __init__(self):
        # Default constructor
        self.state = None
        self.n_player = -1
        self.thinking_time = -1
        self.board = None
        self.myPlayer = None
        self.myColor = None
        self.myShape = None
    
    '''PARAMETER INPUT
    - state, atr: board, players, round (!!)
    - n_player: player 1 ato 2 (0->player 1, 1->player 2)
    - thinking_time: 3s'''

    def setAttribute(self, state: State, n_player: int, thinking_time: float):
        self.state = state
        self.n_player = n_player
        self.thinking_time = time() + thinking_time
        self.board = self.state.board
        self.myPlayer = self.state.players[n_player]
        self.myColor = self.state.players[n_player].color
        self.myShape = self.state.players[n_player].shape

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.setAttribute(state, n_player, thinking_time)
        chosencol, chosenShape = self.pickBestMove()
        best_movement = (chosencol, chosenShape)
        print("choosen col & shape:",chosencol, chosenShape)
        return best_movement

    # fungsi mengecek apakah posisi valid
    def isValidLocation(self, row, col):
        return self.board[row,col].shape == ShapeConstant.BLANK

    # fungsi generate semua kolom yang mungkin ditempati -> arr
    def generateValidLocation(self):
        nrow = self.board.row
        ncol = self.board.col

        availIdx = []

        for col in range(ncol):
            for row in range (nrow-1,-1,-1):
                if self.isValidLocation(row, col):
                    availIdx.append([row,col])
                    break
        
        return availIdx

    '''WORK'''
    def generateASuccessor(self):
        availSpot = self.generateValidLocation()
        return random.choice(availSpot)

    def pickBestMove(self):
        
        validLocations = self.generateValidLocation()
        print("valid loc", validLocations)
        bestScore = 0 # 0 instead of -10000
        bestCol= self.generateASuccessor()[1]

        myPlayer = self.myPlayer
        shape = myPlayer.shape

        for location in validLocations: #[row, col]
            col = location[1]
            
            '''taroh shape disini'''
            shape, score = self.whatShapeandCol(col)
            if score >= bestScore:
                bestScore = score
                bestCol = col
        return bestCol, shape

    def scorePosition(self, state:State):
        score = 0
        
        myPlayer = self.myPlayer
        myShape = myPlayer.shape
        myColor = myPlayer.color

        myPiece = Piece(myShape, myColor)
        npmatrix = np.array(state.board.board)

        center_array = npmatrix[:, state.board.col//2]
        center_count = self.countPieceandEmpty(center_array, myPiece)[0]
        score += center_count * 3

        # Score horizontal
        for r in range(self.board.row):
            row_array = npmatrix[r,:] 

            for c in range(self.board.col - 3):
                window = row_array[c:c+4]
                score += self.evaluatePosition(window, state)
        
        # Score Vertical
        for c in range(self.board.col):
            col_array = npmatrix[:,c] 
            for r in range(self.board.row - 3):
                window = col_array[r:r+4]
                score += self.evaluatePosition(window, state)
        
        # Score diagonal
        for r in range (self.board.row - 3):
            for c in range (self.board.col - 3):
                window = [npmatrix[r+i][c+i] for i in range(4)]
                score += self.evaluatePosition(window, state)

        for r in range (self.board.row - 3):
            for c in range (self.board.col - 3):
                window = [npmatrix[r+3-i][c+i] for i in range(4)]
                score += self.evaluatePosition(window, state)

        return score

    def evaluatePosition(self, window, state):
        score = 0

        myPlayer = self.myPlayer
        myShape = myPlayer.shape
        myColor = myPlayer.color

        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        opp = state.players[n_opp]
        oppShape = opp.shape
        oppColor = opp.color

        combo1 = Piece(myShape, myColor)
        combo2 = Piece(myShape, oppColor)
        combo3 = Piece(oppShape, myColor)
        combo4 = Piece(oppShape, oppColor)
        
        allCombo1 = self.countPieceandEmpty(window, combo1) 
        allCombo2 = self.countPieceandEmpty(window, combo2)
        allCombo3 = self.countPieceandEmpty(window, combo3)
        allCombo4 = self.countPieceandEmpty(window, combo4)

        countCombo1 = allCombo1[0]        
        countCombo2 = allCombo2[0]        
        countCombo3 = allCombo3[0]        
        countCombo4 = allCombo4[0]    
        emptyCombo1 = allCombo1[1]        
        emptyCombo2 = allCombo2[1]        
        emptyCombo3 = allCombo3[1]        
        emptyCombo4 = allCombo4[1]    
        countmyShape = countCombo1 + countCombo2
        countmyColor = countCombo1 + countCombo3
        countoppShape = countCombo3 + countCombo4
        countoppColor = countCombo2 + countCombo2
        emptymyShape = emptyCombo1 + emptyCombo2
        emptymyColor = emptyCombo1 + emptyCombo3
        emptyoppShape = emptyCombo3 + emptyCombo4
        emptyoppColor = emptyCombo2 + emptyCombo2
        if (countmyColor == 4 or countmyShape == 4):
            score += 100000000000000000
        elif (countmyShape==3 and emptymyShape==2):
            score += 300000000000
        elif (countmyShape==2 and emptymyShape==4):
            score += 20000000
        elif (countmyColor==3 and emptymyColor==2): 
            score += 299999999999
        elif (countmyColor==2 and emptymyColor==4):
            score += 19999999
        if (countoppShape==3 and emptyoppShape==2):
            score += -900000000000
        elif (countoppShape==2 and emptyoppShape==4):
            score += -500000000000
        if (countoppColor==3 and emptyoppColor==2):
            score += -899999999999
        elif (countoppColor==2 and emptyoppColor==4):
            score += -499999999999
        if (countoppShape==3 and emptyoppShape==0):
            score += 800000000000
        elif (countoppShape==2 and emptyoppShape==2):
            score += 400000000000
        elif (countoppShape==2 and emptyoppShape==0): # kayaknya penting
            score += 500000000000
        if (countoppColor==3 and emptyoppColor==0):
            score += 799999999999
        elif (countoppColor==2 and emptyoppColor==2):
            score += 399999999999
        elif (countoppColor==2 and emptyoppColor==0): # kayaknya penting
            score += 499999999999
        return score

    def whatShapeandCol(self, col):

        myShape = self.myShape

        # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        opp = self.state.players[n_opp]
        oppShape = opp.shape

        temp_state1 = deepcopy(self.state) # deep copy
        temp_state2 = deepcopy(self.state)

        place(temp_state1, self.n_player, oppShape, col)
        score1 = self.scorePosition(temp_state1)
        
        place(temp_state2, self.n_player, myShape, col)
        score2 = self.scorePosition(temp_state2)
        
        if self.myPlayer.quota[self.myShape] > 0:
            return myShape, score2
        else:
            return oppShape, score1

    def countPieceandEmpty(self, window, piece:Piece):
        count = 0
        empty = 0
        for i in range(len(window)):
            if(window[i].shape == piece.shape and window[i].color == piece.color):
                count += 1
            if(window[i].shape == ShapeConstant.BLANK):
                empty += 1
        return (count, empty)

    # return empty, count
    def countColor(self, window, color):
        count = 0
        empty = 0
        for i in range(len(window)):
            if window[i].color == color:
                count += 1
            if(window[i].shape == ShapeConstant.BLANK):
                empty += 1
        return count, empty

    # return empty, count
    def countShape(self, window, shape):
        count = 0
        empty = 0
        for i in range(len(window)):
            if window[i].shape == shape:
                count += 1
            if(window[i].shape == ShapeConstant.BLANK):
                empty += 1
        return count, empty