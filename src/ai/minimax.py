from time import time
from copy import deepcopy
import numpy as np

from src.constant import ShapeConstant
from src.model import State, piece
from src.model.piece import Piece
from src.utility import *

from typing import Tuple, List

class Minimax:
    def __init__(self):
        pass
       
    def isValidLocation(self, row, col):
         return self.board[row,col].shape == ShapeConstant.BLANK

    def availablemove(self, board : Board):
        nrow = board.row
        ncol = board.col

        availIdx = []

        for col in range(ncol):
            for row in range (nrow-1,-1,-1):
                if self.isValidLocation(row, col):
                    availIdx.append([row,col])
                    break
        
        return availIdx

    def countPieceandEmpty(self, window, piece:Piece):
        count = 0
        empty = 0
        for i in range(len(window)):
            if(window[i].shape == piece.shape and window[i].color == piece.color):
                count += 1
            if(window[i].shape == ShapeConstant.BLANK):
                empty += 1
        return (count, empty)

    def utility(self, state:State):
        window = np.array(state.board.board)

        score = 0

        myPlayer = self.myPlayer
        myShape = myPlayer.shape
        myColor = myPlayer.color

        # OPPONENT
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
            score += 1000000000000
        elif (countmyShape==3 and emptymyShape==2):  
            score += 5
        elif (countmyShape==2 and emptymyShape==4):
            score += 3
        elif (countmyColor==3 and emptymyColor==2): 
            score += 4
        elif (countmyColor==2 and emptymyColor==4):
            score += 2

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
        elif (countoppShape==2 and emptyoppShape==0): 
            score += 500000000000
        if (countoppColor==3 and emptyoppColor==0):
            score += 799999999999
        elif (countoppColor==2 and emptyoppColor==2):
            score += 399999999999

        elif (countoppColor==2 and emptyoppColor==0): 
            score += 499999999999
        return score

    def terminatestate(self, state:State):
        akhir = False
        if (is_win(state.board) or is_full(state.board)):
            akhir = True
        
        return akhir

    def maximizealpha(maxi, availmove, state, depth, a, b, pathhasil):
        bestescore = -10000
        bestepath = None

        for move in availmove:
            copystate = deepcopy(state)
            tempatin = place(copystate, self.n_player, move[1], move[0])
            if tempatin != -1:
                #panggil minimax lagi
                path, score = self.minimaxpruning(not(maxi), availmove, copystate, depth-1, a, b, copyjalur)
                if score > bestescore:
                    bestepath = path
                    bestescore = score
                
                #kalo kelamaan mikir
                if time() > self.thinking_time:
                    return bestepath, bestescore
                
                a = max(bestepath, a)
                if a > b:
                    break

        return bestepath, bestescore

    def minimizebeta(maxi, availmove, state, depth, a, b, pathhasil):
        bestescore = 10000
        bestepath = None

        for move in availmove:
            copystate = deepcopy(state)
            tempatin = place(copystate, self.other_player, move[1], move[0])
            if tempatin != -1:
                #panggil minimax lagi
                copyjalur = deepcopy(pathhasil)
                copyjalur.append(move, tempatin)
                path, score = self.minimax(not(maxi), availmove, copystate, depth-1, a, b, copyjalur)
                if score < bestescore:
                    bestepath = path
                    bestescore = score
                
                if time() > self.thinking_time:
                    return bestepath, bestescore
                
                b = min(bestepath, b)
                if a > b:
                    break

        return bestepath, bestescore

    def minimaxpruning(maxi, availmove, state : State, depth, a, b, pathhasil):
        #list availmove
        availmove = availablemove(board)

        #nilai awal alpha beta
        a = -10000
        b = 10000

        #hasil algoritma
        pathhasil = []        
        bestescoreminimax = 0
        bestepathminimax = None

        #cek dah terminatestate belom 
        if (depth == 0 or self.terminatestate(state)):
            return pathhasil, self.utility(state)
            
        if maxi:
            #panggil maximizealpha
            self.maximizealpha(maxi, availmove, state, depth, a, b, pathhasil)
        else:#not maxi
            #panggil minimizebeta
            self.minimizebeta(maxi, availmove, state, depth, a, b, pathhasil)

        return bestepathminimax, bestescoreminimax
        
    
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.n_player = n_player
        if n_player == 0:
            self.other_player = 1
        else:
            self.other_player = 0
        
        self.best_move = None

        jalur, score = self.minimax()

        return jalur[0][0]
