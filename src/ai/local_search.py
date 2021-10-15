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

        # Nambahin atribut
        # setattr(self, 'myPlayer', self.state.players[n_player])
        # setattr(self, 'myShape', self.state.players[n_player].shape)
        # setattr(self, 'myColor', self.state.players[n_player].color)

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

        ## TODO score center column
        center_array = []

        ## tes ngeprint board pake str; WORK
        # print("BOARDDD")
        # state.board.board[5][0].print()
        # for mat in state.board.board:
        #     for m in mat:
        #         m.print()
        
        # convert jadi numpy array
        npmatrix = np.array(state.board.board)

        # tes ngeprint board pas pake numpy
        # print("NPMATRIX",list(npmatrix))

        ## score horizontal
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
        return score

    def evaluatePosition(self, window, state):
        score = 0

        myPlayer = self.myPlayer
        myShape = myPlayer.shape
        myColor = myPlayer.color

        # diasumsiin ngitung yang warna DAN shape nya sama
        myPiece = Piece(myShape, myColor)
        
        # print("myPiece")
        # myPiece.print()

        countAll = self.countPieceandEmpty(window, myPiece)

        # print("COUNT ALL:", countAll)

        count = countAll[0]
        empty = countAll[1]

        # OPPONENT
        n_opp = 1

        if self.n_player == 1:
            n_opp = 0
        
        opp = state.players[n_opp]
        oppShape = opp.shape
        oppColor = opp.color
        oppPiece = Piece(oppShape, oppColor)

        countOppAll = self.countPieceandEmpty(window, oppPiece)
        countOpp = countOppAll[0]
        emptyOpp = countOppAll[1]

        if count == 4:
            score += 100
        elif count == 3 and empty == 1:
            score += 5
        elif count == 2 and empty == 2:
            score +=2
        
        if countOpp == 3 and emptyOpp == 1:
            score -= 4

        # print("SCORE:",score) # kenapa 0 ya ngab
        
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

