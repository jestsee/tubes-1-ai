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
        pass

    # parameter input:
    # state, atr: board, players, round (!!)
    # n_player: player 1 ato 2 (0->player 1, 1->player 2)
    # thinking_time: 3s
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        myPlayer = state.players[n_player]
        # myPiece = piece(myPlayer.shape, myPlayer.color)
        choosencol = self.pickBestMove(state.board, n_player, state)
        best_movement = (choosencol, myPlayer.shape)
        
        # buat debug
        print("choosen col:",choosencol)

        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        # NOTE 
        # yang di-return adalah nomor kolom dan bentuk shape
        # Player 1 RED, O
        # Player 2 BLUE, X

        return best_movement

    # gimana cara pass info player kesini?
    # tau kuota masing2 piece darimana? state -> players[n_player]

    # TODO fungsi untuk menentukan nilai heuristik

    '''WORK'''
    # fungsi mengecek apakah posisi valid
    def isValidLocation(self, row, col, board:Board):
        return board[row,col].shape == ShapeConstant.BLANK

    '''DAH WORK'''
    # fungsi generate semua kolom yang mungkin ditempati -> arr
    def generateValidLocation(self, board: Board):
        nrow = board.row
        ncol = board.col

        availIdx = []

        for col in range(ncol):
            for row in range (nrow-1,-1,-1):
                if self.isValidLocation(row, col, board):
                    availIdx.append([row,col])
                    break
        
        return availIdx

    '''WORK HARUSNYA'''
    # generate 1 random suksesor --> [row, col]
    def generateASuccessor(self, board: Board):
        availSpot = self.generateValidLocation(board)
        return random.choice(availSpot)

    # dapetin nilai heuristik dari suatu posisi 
    def getHeuristicValue(self, row, col, n_player, state: State):
        myPlayer = state.players[n_player]
        myShape = myPlayer.shape
        myColor = myPlayer.color

        # TODO belom kelar

    def pickBestMove(self,board, n_player, state:State):
        
        validLocations = self.generateValidLocation(board)
        print("valid loc", validLocations)
        bestScore = -10000
        bestCol= self.generateASuccessor(board)[1]

        myPlayer = state.players[n_player]
        myShape = myPlayer.shape
        myColor = myPlayer.color

        # misalnya baru cobain warna dulu
        piece = Piece(myShape, myColor)

        for location in validLocations: #[row, col]
            col = location[1]
            row = self.getNextOpenRow(board, col)
            # print("GET NEXT OPEN ROW",row)

            temp_board = deepcopy(board) # deep copy
            # temp_board = Board(board.row, board.col)
            # temp_board.board = board.board.copy()

            temp_board.set_piece(row, col, piece)
            # temp = place(state, n_player, myShape, col)
            # print("PLACE",temp)
            score = self.scorePosition(temp_board, n_player, state)

            if score > bestScore:
                bestScore = score
                bestCol = col

        return bestCol

    # ngikut youtube Keith Galli; rename jadi getNextValidRow?
    # nyari row yang valid berdasarkan col yang sudah ada
    def getNextOpenRow(self, board:Board, col):
        for r in range(board.row-1,-1,-1):
            if self.isValidLocation(r,col,board):
                return r

    def scorePosition(self, board:Board, n_player, state:State):
        score = 0
        
        myPlayer = state.players[n_player]

        ## TODO score center column
        center_array = []
        
        # convert jadi numpy array
        npmatrix = np.matrix(board.board)

        ## score horizontal
        for r in range(board.row):
            # get all the piece in the column position for row r
            row_array = list(npmatrix[r,:])
            for c in range(board.col-3):
                window = row_array[c:c+4]
                score += self.evaluatePosition(window, n_player, state)
        return score

    def evaluatePosition(self, window, n_player, state:State):
        score = 0

        # mungkin ini entar diapain gitu biar ga redundan
        myPlayer = state.players[n_player]
        myShape = myPlayer.shape
        myColor = myPlayer.color

        # diasumsiin ngitung yang warna DAN shape nya sama
        myPiece = Piece(myShape, myColor)
        count = self.countPieceandEmpty(window, myPiece)[0]
        empty = self.countPieceandEmpty(window, myPiece)[1]

        # opponent's
        n_opp = 1

        if n_player == 1:
            n_opp = 0
        
        opp = state.players[n_opp]
        oppShape = opp.shape
        oppColor = opp.color
        oppPiece = Piece(oppShape, oppColor)
        countOpp = self.countPieceandEmpty(window, oppPiece)
        emptyOpp = self.countPieceandEmpty(window, oppPiece)


        if count == 4:
            score += 100
        elif count == 3 and empty == 1:
            score += 5
        elif count == 2 and empty == 2:
            score +=2
        
        if countOpp == 3 and emptyOpp == 1:
            score -= 4
        
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

