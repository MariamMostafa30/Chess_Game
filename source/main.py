from tkinter import Tk
import chess
from source.GUI import GUI
from tkinter import messagebox
import  source.AI

class Chess_Board:

    ROOT = Tk()
    ROOT.title("Chess Game")
    BOARD = chess.Board()
    SLOT = [True]     #True = white player's turn ,,  False = "black player" Machine's turn

    #Initialize the game then start playing
    def __init__(ChessFrame):
        ChessFrame.display = GUI(ChessFrame, ChessFrame.ROOT, ChessFrame.BOARD, ChessFrame.SLOT)
        ChessFrame.display.pack()

    #Start of the game
    def start(ChessFrame):
        if(ChessFrame.SLOT[0] == False):
            ChessFrame.AIplay()
        ChessFrame.ROOT.mainloop()

    def AIplay(ChessFrame): #Machine's turn
        if(ChessFrame.BOARD.is_checkmate()):  #Check the status at the end of the game
            messagebox.showwarning("End game", "You win")
            ChessFrame.display.canvas.delete("status")
            ChessFrame.display.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                                            text="Status Board: Your Win", tag="status")
        elif(ChessFrame.BOARD.is_stalemate() or ChessFrame.BOARD.can_claim_threefold_repetition() or ChessFrame.BOARD.is_insufficient_material() or ChessFrame.BOARD.is_fivefold_repetition()):
            messagebox.showwarning("End game", "Draw")
            ChessFrame.display.canvas.delete("status")
            ChessFrame.display.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                                            text="Status Board: Draw", tag="status")
        else:
            #Check if the machine will play
            if(ChessFrame.SLOT[0] == False):
            #Checks best option for machine using Alpha-Beta Algorithm and depth = 3
                machineMove = source.AI.makeBestMove(3, ChessFrame.BOARD, True)
                move = chess.Move.from_uci(machineMove)
                ChessFrame.BOARD.push(move)
                ChessFrame.display.canvas.delete("move")
                ChessFrame.display.canvas.create_text(20, 150, anchor='w', font="VNI-Dom 14",
                                        text="Black Move: " + str(move), tag="move")
            print(ChessFrame.BOARD)
            ChessFrame.display.draw()

            #Checks the status of the game after the move
            if (ChessFrame.BOARD.is_checkmate()):
                messagebox.showwarning("End game", "Machine win")
                ChessFrame.display.canvas.delete("status")
                ChessFrame.display.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                                        text="Status Board: Machine Win", tag="status")
            elif (ChessFrame.BOARD.is_stalemate() or ChessFrame.BOARD.can_claim_threefold_repetition() or ChessFrame.BOARD.is_insufficient_material() or ChessFrame.BOARD.is_fivefold_repetition()):
                messagebox.showwarning("End game", "Draw")
                ChessFrame.display.canvas.delete("status")
                ChessFrame.display.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                                        text="Status Board: Draw", tag="status")
            else:
                ChessFrame.SLOT[0] = True
                ChessFrame.display.canvas.delete("status")
                ChessFrame.display.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                                        text="Status Board: Your Turn", tag="status")


#Start the game
game = Chess_Board()
game.start()