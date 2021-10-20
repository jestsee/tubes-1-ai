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

import math
#TODO: caranya block serangan lawan?
#TODO: terapin algo stochastic nya? krn pickBestMove msh pake steepest ascent
#TODO: cara botnya main masih kayak connect4, 
    #  hanya ngeluarin bidak yang sama kayak shape dan color dia
#TODO: modif lagi fungsi heuristiknya
#TODO: belom nanganin kasus kalo mikirnya lebih dari 3s

class MinimaxGroup37:
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

        # chosencol, chosenShape = self.pickBestMove()
        # best_movement = (chosencol, chosenShape)
        
        # buat debug
        # print("choosen col & shape:",chosencol, chosenShape)

        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        # NOTE 
        # yang di-return adalah nomor kolom dan bentuk shape
        # Player 1 RED, O
        # Player 2 BLUE, X

        pls = self.minimax(self.state, 4, -math.inf, math.inf, True)
        print("PLS",pls)
        best_movement = (pls[0], pls[2])

        return best_movement

    '''WORK'''
    # fungsi mengecek apakah posisi valid
    def isValidLocation(self, row, col):
        return self.board[row,col].shape == ShapeConstant.BLANK

    '''WORK'''
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
    # generate 1 random suksesor --> [row, col]
    def generateASuccessor(self):
        availSpot = self.generateValidLocation()
        return random.choice(availSpot)

    def scorePosition(self, state:State):
        score = 0
        
        myPlayer = self.myPlayer
        myShape = myPlayer.shape
        myColor = myPlayer.color

        myPiece = Piece(myShape, myColor)

        ## tes ngeprint board pake str; WORK
        # print("BOARDDD")
        # state.board.board[5][0].print()
        # for mat in state.board.board:
        #     for m in mat:
        #         m.print()
        
        # convert jadi numpy array
        npmatrix = np.array(state.board.board)

        # Score center column - ngutamain buat isi kolom tengah
        center_array = npmatrix[:, state.board.col//2]
        center_count = self.countPieceandEmpty(center_array, myPiece)[0]
        score += center_count * 3

        # Score horizontal
        for r in range(self.board.row):
            # get all the piece in the column position for row
            row_array = npmatrix[r,:] 
            # row_array = [Piece(i) for i in row_array ]
            # print("row array:",row_array)

            for c in range(self.board.col - 3):
                window = row_array[c:c+4]

                '''WORK'''
                # print("WINDOW PLS:", window[0].color, window[0].shape)

                score += self.evaluatePosition(window, state)
        
        # Score Vertical
        for c in range(self.board.col):
            col_array = npmatrix[:,c] 
            for r in range(self.board.row - 3):
                window = col_array[r:r+4]
                score += self.evaluatePosition(window, state)
        
        # Score diagonal
        ## TODO ini work ga ya? wkwkw
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
        allCombo2 = self.countPieceandEmpty(window, combo2) # myShape oppColor
        allCombo3 = self.countPieceandEmpty(window, combo3) # oppShape myColor
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
        # color / shape 4
        if (countmyColor == 4 or countmyShape == 4):
            score += 100000000000000000 # sebanyaknya
        # ga sepenting ngeblock lawan
        elif (countmyShape==3 and emptymyShape==2):  # 1 kosong sama 2 2nya jadi dikali 2
            score += 300000000000
        elif (countmyShape==2 and emptymyShape==4):
            score += 20000000
        elif (countmyColor==3 and emptymyColor==2): 
            score += 299999999999
        elif (countmyColor==2 and emptymyColor==4):
            score += 19999999
        # jangan sampe ada empty pas ada 3!
        if (countoppShape==3 and emptyoppShape==2):
            score += -900000000000
        elif (countoppShape==2 and emptyoppShape==4):
            score += -500000000000
        if (countoppColor==3 and emptyoppColor==2):
            score += -899999999999
        elif (countoppColor==2 and emptyoppColor==4):
            score += -499999999999
        # ngeblocking
        # jangan sampe ada empty pas ada 3!
        if (countoppShape==3 and emptyoppShape==0): #ditutup
            score += 800000000000
        # satu aja cukup, sisanya fokus yg lain aja, eh tp belom tau sih
        elif (countoppShape==2 and emptyoppShape==2):
            score += 400000000000
        elif (countoppShape==2 and emptyoppShape==0): # kayaknya penting
            score += 500000000000
        if (countoppColor==3 and emptyoppColor==0):
            score += 799999999999
        elif (countoppColor==2 and emptyoppColor==2):
            score += 399999999999
        # cukup satu aja yg counter
        elif (countoppColor==2 and emptyoppColor==0): # kayaknya penting
            score += 499999999999
        return score

    def whatShapeandCol(self, col):
        # TODO: belom nanganin kasus kalo piece abis

        myShape = self.myShape

        # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        opp = self.state.players[n_opp]
        oppShape = opp.shape

        temp_state1 = deepcopy(self.state) # deep copy
        temp_state2 = deepcopy(self.state)

        # dahuluin taroh shape lawan
        place(temp_state1, self.n_player, oppShape, col)
        score1 = self.scorePosition(temp_state1)
        
        # print("score shape lawan:", score1)
        # print(temp_state1.board)
        # print("\n")

        place(temp_state2, self.n_player, myShape, col)
        score2 = self.scorePosition(temp_state2)

        # print("score shape kita:", score2)
        # print(temp_state2.board)
        # print("\n")
        
        if self.myPlayer.quota[self.myShape] > 0:
            return myShape, score2
        else:
            return oppShape, score1

        '---'
    
        '---'

        # kalo shape lawan ga menimbulkan kerugian langsung return
        # if score1 >= 0:
        #     return oppShape, score1

        # # kalo rugi, taroh shape kita
        # else:
        #     # taroh shape kita
        #     place(temp_state2, self.n_player, myShape, col)
        #     score2 = self.scorePosition(temp_state2)

        #     return myShape, score2
        
    # kalo misalnya udah mix O sama X dari pihak merah, botnya jadi aneh, kalo O dia oke" aja keknya

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

    def minimax(self, state:State, depth, alpha, beta, maximizingPlayer):
         # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        myPiece = Piece(self.myShape, self.myColor)
        oppPiece = Piece(self.state.players[n_opp].shape, state.players[n_opp].color)

        myPieceOppShape = Piece(state.players[n_opp].shape, self.myColor)
        oppPieceMyShape = Piece(self.myShape, state.players[n_opp].color)

        shape = self.whatShape()

        # print("BOARDDD")
        # print(state.board)

        validLocations = self.generateValidLocation()
        isTerminal = self.isTerminal(state)
        if depth == 0 or isTerminal:
            
            if isTerminal:
                if self.winningMove(state, myPiece) or self.winningMove(state, myPieceOppShape):
                    return (None, 100000000000000, shape) # shapenya return none?
                elif self.winningMove(state, oppPiece) or self.winningMove(state,oppPieceMyShape):
                    return (None, -100000000000000, shape)
                else:
                    print("MASUK KE GAME OVER")
                    return (None,0,None)
            else:
                # depth is zero
                return(None, self.scorePosition(state), shape)
        
        if maximizingPlayer:
            # print("MASUK BESAR")
            value = -math.inf
            column = self.generateASuccessor()

            for valid in validLocations:
                col = valid[1]
                s_copy = deepcopy(state)
                place(s_copy, self.n_player, shape, col)
                newScore = self.minimax(s_copy, depth-1, alpha, beta, False)[1]
                shape = self.whatShape()
                if newScore > value:
                    value = newScore
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value, shape
        
        else:
            # minimizing player
            # print("MASUK MINI")
            value = math.inf
            column = self.generateASuccessor()

            for valid in validLocations:
                col = valid[1]
                s_copy = deepcopy(state)

                # check opponent's
                opponent = state.players[n_opp]
                oppShape = self.myShape
                if opponent.quota[opponent.shape] > 0:
                    oppShape = opponent.shape

                place(s_copy, n_opp, oppShape, col)
                newScore = self.minimax(s_copy, depth-1, alpha, beta, True)[1]
                shape = self.whatShape()
                if newScore < value:
                    value = newScore
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value, shape


    def winningMove(self, state:State, piece:Piece):
        # horizontal
        for c in range(self.board.col-3):
            for r in range(self.board.row):
                # semua shapenya sama
                if state.board[r,c].shape == piece.shape and state.board[r,c+1].shape == piece.shape and state.board[r,c+2].shape == piece.shape and state.board[r,c+3].shape == piece.shape:
                    return True
                
                # semua warnanya sama
                if state.board[r,c].color == piece.color and state.board[r,c+1].color == piece.color and state.board[r,c+2].color == piece.color and state.board[r,c+3].color == piece.color:
                    return True
        
        # vertical
        for c in range(self.board.col):
            for r in range(self.board.row-3):
                # semua shapenya sama
                if state.board[r,c].shape == piece.shape and state.board[r+1,c].shape == piece.shape and state.board[r+2,c].shape == piece.shape and state.board[r+3,c].shape == piece.shape:
                    return True
                
                # semua warnanya sama
                if state.board[r,c].color == piece.color and state.board[r+1,c].color == piece.color and state.board[r+2,c].color == piece.color and state.board[r+3,c].color == piece.color:
                    return True
        
        # diagonal 1
        for c in range(self.board.col-3):
            for r in range(self.board.row-3):
                # semua shapenya sama
                if state.board[r,c].shape == piece.shape and state.board[r+1,c+1].shape == piece.shape and state.board[r+2,c+2].shape == piece.shape and state.board[r+3,c+3].shape == piece.shape:
                    return True
                
                # semua warnanya sama
                if state.board[r,c].color == piece.color and state.board[r+1,c+1].color == piece.color and state.board[r+2,c+2].color == piece.color and state.board[r+3,c+3].color == piece.color:
                    return True
        
        # diagonal 2
        for c in range(self.board.col-3):
            for r in range(3, self.board.row):
                # semua shapenya sama
                if state.board[r,c].shape == piece.shape and state.board[r-1,c+1].shape == piece.shape and state.board[r-2,c+2].shape == piece.shape and state.board[r-3,c+3].shape == piece.shape:
                    return True
                
                # semua warnanya sama
                if state.board[r,c].color == piece.color and state.board[r-1,c+1].color == piece.color and state.board[r-2,c+2].color == piece.color and state.board[r-3,c+3].color == piece.color:
                    return True

    def isTerminal(self, state:State):
         # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        myPiece = Piece(self.myShape, self.myColor)
        oppPiece = Piece(state.players[n_opp].shape, state.players[n_opp].color)

        myPieceOppShape = Piece(state.players[n_opp].shape, self.myColor)
        oppPieceMyShape = Piece(self.myShape, state.players[n_opp].color)

        return self.winningMove(state, myPiece) or self.winningMove(state, oppPiece) or self.winningMove(state, myPieceOppShape) or self.winningMove(state, oppPieceMyShape) or len(self.generateValidLocation()) == 0
    
    def whatShape(self):
        # prioritasin shape kita dulu
        # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0

        opp = self.state.players[n_opp]
        oppShape = opp.shape

        if self.myPlayer.quota[self.myShape] > 0:
            return self.myShape
        else:
            return oppShape