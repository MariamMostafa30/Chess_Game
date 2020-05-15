import source.table
import chess
import math
import source.table

import chess.polyglot

from source import table

isExistInOpeningBook = True;

def makeBestMove(depth, chess_board, isMaximisingPlayer): # using minimax algorithm
    exMove = experienceMove(chess_board);
    if exMove is None:
        return minimax(depth, chess_board, isMaximisingPlayer); #  is maximising player which mean that is the black player our algorithm
    else:
        return exMove;


def experienceMove(chess_board):
    with chess.polyglot.open_reader("../data/opening/OpeningBook.bin") as reader:
        # polyglot allows UCI(universal chess interface that is using to open a communication protocol to play tha game automatically)
        # so polyglot ALLOWS UCI to  use interfaces  and support GUI
        # that is for opening a book to  find  all entries for the starting position bm3na kol moves el momkn yt7arkha mn position dah
        # opening book is the chess book that  have all move strategies
        opening_moves = [
            str(entry.move) for entry in reader.find_all(chess_board)
        ];
        if opening_moves: # if opening moves don't equal to null
            for move in opening_moves: # then do foreach move in openingmoves we will return move

                return move
        else:
            return None


def minimax(depth, chess_board, isMaximisingPlayer): # minimax with alpha-beta algorithm
    legal_moves = [str(legal_move) for legal_move in chess_board.legal_moves]; # i want legalmove foreach legal move in legal moves
   # that will return the copy of all legal moves
    bestMove = -math.inf; # maxvalue
    bestMoveFound = "abc";  # any initialization

    for newMove in legal_moves: # foreach newmove in legal moves which means that the player chose the new one of the existed legal moves
        chess_board.push(chess.Move.from_uci(newMove)); # i will move the piece to another tile according to my legal move and as we said , the uci is the universal chess interface
        value = Alpha_Beta(depth - 1, chess_board, -math.inf, math.inf, not (isMaximisingPlayer));
        chess_board.pop();
        if (value >= bestMove):
            bestMove = value;
            bestMoveFound = newMove;

    return bestMoveFound;

 # Notice that if alpha greater than beta it will pruning otherwise ,it will continue searching for bestmove
def Alpha_Beta(depth, chess_board, alpha, beta, isMaximisingPlayer): # alpha support max value so  at first initial it will take the lowest value to compare it with current values that cause of min or beta the opponent
    if (depth == 0): # that happens in two cases,  when the game is over or the node is a leaf node
        return -evaluateBoard(chess_board);

    legal_moves = [str(legal_move) for legal_move in chess_board.legal_moves];

    if (isMaximisingPlayer):  #  if the black player will play
        bestMove = -math.inf; # initial the highestvalue  with smallestvalue
        for newMove in legal_moves:
            chess_board.push(chess.Move.from_uci(newMove));
            # if there is  a legal move then updates the position with that move  in the suitable tile on the board and push it in the move stack
            bestMove = max(bestMove, Alpha_Beta(depth - 1, chess_board, alpha, beta, not isMaximisingPlayer));
            # here , we used the recursive because min caused max and vice versa
            chess_board.pop(); # pop the move from move stack
            alpha = max(alpha, bestMove); # return the highest value
            if beta <= alpha: # Pruning
                return bestMove;

        return bestMove;

    else:
         # if the white player play  not the maximisingplayer "black"
        bestMove = math.inf; # we initialize it with highest value
        for newMove in legal_moves:
            chess_board.push(chess.Move.from_uci(newMove));
            bestMove = min(bestMove, Alpha_Beta(depth - 1, chess_board, alpha, beta, not isMaximisingPlayer)); # that will return the smallest value from all items that is compare with
            chess_board.pop(); # unmake the move
            beta = min(beta, bestMove);  # we initial the beta variable with the smallest value that returns from comparing best move value with old beta
            if beta <= alpha:
                return bestMove;

        return bestMove;


def evaluateBoard(chess_board):
    totalEvaluation = 0;
    for square in chess.SQUARES:
        totalEvaluation += getPieceValue(chess_board, square);
        # heuristic function, every piece has heuristic value which  tell us how likely do we win or lose
    return totalEvaluation;


def isEndgame(chess_board):
    for square in chess.SQUARES:
        if isHeavyPiece(chess_board, square):
            return False

    return True

def isHeavyPiece(chess_board, square):
    piece = chess_board.piece_at(square)
    if piece is None:
        return False
    # check if the piece is rook or queen
    if piece.symbol().lower() == 'q' or piece.symbol().lower() == 'r':
        return True
    else:
        return False



def getPieceValue(chess_board, square): # to evaluate board
    piece = chess_board.piece_at(square);
    if piece is None: # if there is a piece into that tile
        return 0;

    def getAbsoluteValue(piece, isWhite, square):
        row = convert_square(square)[0]
        col = convert_square(square)[1]
        if piece.symbol().lower() == 'p':
            return 100 + (source.table.pawnEvalWhite[row][col] if isWhite else source.table.pawnEvalBlack[row][col]);
        elif piece.symbol().lower() == 'n':
            return 320 + source.table.knightEval[row][col];
        elif piece.symbol().lower() == 'b':
            return 330 + (source.table.bishopEvalWhite[row][col] if isWhite else source.table.bishopEvalBlack[row][col]);
        elif piece.symbol().lower() == 'r':
            return 500 + (source.table.rookEvalWhite[row][col] if isWhite else source.table.rookEvalBlack[row][col]);
        elif piece.symbol().lower() == 'q':
            return 900 + source.table.evalQueen[row][col];
        elif piece.symbol().lower() == 'k':
            if isEndgame(chess_board):
                return 20000 + (table.KingWhiteEndgame[row][col] if isWhite else table.KingBlackEndgame[row][col]);
            else:
                return 20000 + (table.kingEvalWhite[row][col] if isWhite else table.kingEvalBlack[row][col]);


    absoluteValue = getAbsoluteValue(piece, chess_board.color_at(square), square);

    return absoluteValue if chess_board.color_at(square) else -absoluteValue;

# here we calculate the square that we found the piece on to determine the piece's position "row+ col"
def convert_square(square):
    row = (square // 8); # ranks each rank has eight  horizontal squares
    column = square % 8; # files each file has eight vertical squares
    return (row, column)



