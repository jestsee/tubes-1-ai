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

#TODO: caranya block serangan lawan?
#TODO: terapin algo stochastic nya? krn pickBestMove msh pake steepest ascent
#TODO: cara botnya main masih kayak connect4, 
    #  hanya ngeluarin bidak yang sama kayak shape dan color dia
#TODO: modif lagi fungsi heuristiknya
#TODO: belom nanganin kasus kalo mikirnya lebih dari 3s

class LocalSearch:
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

        # myPiece = piece(myPlayer.shape, myPlayer.color)
        choosencol = self.pickBestMove()
        best_movement = (choosencol, self.myPlayer.shape)
        
        # buat debug
        print("choosen col:",choosencol)

        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        # NOTE 
        # yang di-return adalah nomor kolom dan bentuk shape
        # Player 1 RED, O
        # Player 2 BLUE, X

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

    def pickBestMove(self):
        
        validLocations = self.generateValidLocation()
        print("valid loc", validLocations)
        bestScore = 0 # 0 instead of -10000
        bestCol= self.generateASuccessor()[1]

        myPlayer = self.myPlayer
        myShape = myPlayer.shape

        for location in validLocations: #[row, col]
            col = location[1]

            temp_state = deepcopy(self.state) # deep copy
            
            '''sampe sini dah bener harusnya'''

            isSuc=place(temp_state, self.n_player, myShape, col)
            score = self.scorePosition(temp_state)

            # print("BOARDDD")
            # print(temp_state.board)
            # print("SCORE: ",score)
            # print("BEST COL - pickBestMove:",bestCol)

            if score > bestScore:
                bestScore = score
                bestCol = col
        return bestCol

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

            for c in range(4):
                window = row_array[c:c+4]

                '''WORK'''
                # print("WINDOW PLS:", window[0].color, window[0].shape)

                score += self.evaluatePosition(window, state)
        
        # Score Vertical
        for c in range(self.board.col):
            col_array = npmatrix[:,c] 
            for r in range(3):
                window = col_array[r:r+4]
                score += self.evaluatePosition(window, state)
        
        # Score diagonal
        ## TODO ini work ga ya? wkwkw
        for r in range (3):
            for c in range (4):
                window = [npmatrix[r+i][c+i] for i in range(4)]
                score += self.evaluatePosition(window, state)

        for r in range (3):
            for c in range (4):
                window = [npmatrix[r+3-i][c+i] for i in range(4)]
                score += self.evaluatePosition(window, state)

        return score

    def evaluatePosition(self, window, state):
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
        
        # print("myPiece")
        # myPiece.print()

        allCombo1 = self.countPieceandEmpty(window, combo1)
        allCombo2 = self.countPieceandEmpty(window, combo2)
        allCombo3 = self.countPieceandEmpty(window, combo3)
        allCombo4 = self.countPieceandEmpty(window, combo4)

        # print("COUNT ALL:", countAll)

        countCombo1 = allCombo1[0]        
        countCombo2 = allCombo2[0]        
        countCombo3 = allCombo3[0]        
        countCombo4 = allCombo4[0]    
        emptyCombo1 = allCombo1[1]        
        emptyCombo2 = allCombo2[1]        
        emptyCombo3 = allCombo3[1]        
        emptyCombo4 = allCombo4[1]    

        if (countCombo1 == 4): #or (countCombo1 + countCombo2 == 4) or (countCombo1 + countCombo3 == 4):
            score += 100
        elif (countCombo1 == 3 and emptyCombo1 == 1): #or (countCombo1 + countCombo2 == 3) or (countCombo1 + countCombo3 == 3):
            score += 5
        elif (countCombo1 == 2 and emptyCombo1 == 2): #or (countCombo1 + countCombo2 == 2) or (countCombo1 + countCombo3 == 2):
            score += 2
        if (countCombo4 == 3 and emptyCombo4 == 1): #or (countCombo3 + countCombo4 == 3) or (countCombo2 + countCombo4 == 3):
            score += -4
        return score

    def countPieceandEmpty(self, window, piece:Piece):
        count = 0
        empty = 0
        for i in range(len(window)):
            if(window[i].shape == piece.shape and window[i].color == piece.color):
                count += 1
            if(window[i].shape == ShapeConstant.BLANK):
                empty += 1
        return (count, empty)