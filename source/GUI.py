import chess
from tkinter import Frame
from tkinter import Canvas
from tkinter import Button
import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox


class GUI(Frame):
    # constant
    NUMBER_COLLUM = 8
    NUMBER_ROW = 8
    SIZE_SQUARE = 64
    WHITE = '#F0D9B5'
    BLACK = '#B58863'
    YELLOW = '#775cff'
    GREEN = '#1eed28'
    YIELD = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    MAP = {'a' : 0, 'b' : 1, 'c' : 2, 'd': 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}



    def __init__(self, game, root, board, slot):
        self.game = game
        self.board = board
        self.slot = slot
        super().__init__(root)
        #data
        self.piece = {}

        #king
        self.icon = Image.open("../data/image/white/K.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['K'] = self.icon

        self.icon = Image.open("../data/image/black/k.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['k'] = self.icon

        #Queen
        self.icon = Image.open("../data/image/white/Q.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['Q'] = self.icon

        self.icon = Image.open("../data/image/black/q.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['q'] = self.icon

        #Rook
        self.icon = Image.open("../data/image/white/R.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['R'] = self.icon

        self.icon = Image.open("../data/image/black/r.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['r'] = self.icon

        #Bishop
        self.icon = Image.open("../data/image/white/B.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['B'] = self.icon

        self.icon = Image.open("../data/image/black/b.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['b'] = self.icon

        #Knight
        self.icon = Image.open("../data/image/white/N.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['N'] = self.icon

        self.icon = Image.open("../data/image/black/n.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['n'] = self.icon

        #Pawn
        self.icon = Image.open("../data/image/white/P.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['P'] = self.icon

        self.icon = Image.open("../data/image/black/p.png")
        self.icon = self.icon.resize((self.SIZE_SQUARE, self.SIZE_SQUARE))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.piece['p'] = self.icon


        self.square = []
        offsetRank = (self.NUMBER_ROW - 1)* self.SIZE_SQUARE
        for i in range(self.NUMBER_ROW):
            for j in range(self.NUMBER_COLLUM):
                self.square.append([j*self.SIZE_SQUARE, offsetRank - i*self.SIZE_SQUARE])



        BoardHeight = self.NUMBER_ROW * self.SIZE_SQUARE
        BoardWith = self.NUMBER_COLLUM * self.SIZE_SQUARE
        self.GUIBoard = Canvas(self, width= BoardWith, height= BoardHeight, background='gray')

        self.GUIBoard.pack(side= tkinter.LEFT)


        self.GUIBoard.bind('<Button-1>', self.click)
        self.clickfrom = None
        self.clickTo = None

        self.coordinateClick = []

        self.listHightLight = []
        self.mapHightLight = []
        self.draw()


        self.controlPanel = Frame(self, width= 300, background = "#d2f0bb")
        self.controlPanel.pack(side=tkinter.LEFT, fill = tkinter.BOTH)


        self.canvas = Canvas(self.controlPanel, background = 'white', height = 256)
        self.canvas.create_text(20, 30, anchor='w', font="VNI-Dom 16",
                           text="Information of game:    ")
        self.canvas.create_text(20, 60, anchor='w', font="VNI-Dom 14",
                           text="Your color piece is white   ")
        self.canvas.create_text(20, 90, anchor='w', font="VNI-Dom 14",
                           text="Color piece of machine is black  ")
        self.canvas.create_text(20, 120, anchor='w', font="VNI-Dom 14",
                           text="Alpha beta pruning depth = 3")
        self.canvas.create_text(20, 150, anchor='w', font="VNI-Dom 14",
                           text="Oponent move: ", tag = "move")
        self.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                           text="Status board: your turn", tag = "status")
        self.canvas.pack(fill=tkinter.BOTH, side = tkinter.TOP)

        self.ButtonNewgame = tkinter.Button(self.controlPanel, text = "New game", width = 10, font="VNI-Dom 14", background = "#1698de")
        self.ButtonNewgame.place(relx = .5, rely = .7, anchor ='c')

        self.ButtonNewgame.bind('<Button-1>', self.clearBoard)


    def clearBoard(self, event):
        self.board.reset()
        self.slot[0] = True
        self.canvas.delete("move")
        self.canvas.create_text(20, 150, anchor='w', font="VNI-Dom 14",
                           text="Oponent move: ", tag = "move")
        self.draw()


    def click(self, event):

        if self.slot[0] == True: # opponent turn
                x = event.x // self.SIZE_SQUARE
                y = self.NUMBER_ROW - event.y // self.SIZE_SQUARE
                self.coordinateClick.clear()
                self.coordinateClick.append(x)
                self.coordinateClick.append(y)
                traceSquare = (self.NUMBER_ROW - 1 - event.y // self.SIZE_SQUARE)*self.NUMBER_ROW + (event.x // self.SIZE_SQUARE)

                if self.clickfrom is None:
                    pieceAt = self.board.piece_at(traceSquare)
                    if pieceAt is not None:
                        self.clickfrom = self.YIELD[self.coordinateClick[0]] + str(self.coordinateClick[1])
                        self.hightLight()
                    else:
                        self.draw()
                else:
                    if traceSquare in self.mapHightLight:
                        self.move()
                    else:
                        self.mapHightLight.clear()
                        self.draw()
                    self.clickfrom = None


    def hightLight(self):
        position = self.YIELD[self.coordinateClick[0]] + str(self.coordinateClick[1])
        legal_moves =[str(legal_move) for legal_move in self.board.legal_moves]
        self.listHightLight.clear()
        self.mapHightLight.clear()
        for legal_move in legal_moves:
            if (position == legal_move[:2]):
                self.listHightLight.append(legal_move)
        for legal_move in self.listHightLight:
            self.mapHightLight.append(self.MAP[legal_move[2]] + (int(legal_move[3]) - 1)*self.NUMBER_ROW)

        self.draw()


    def move(self):
        self.clickTo = self.YIELD[self.coordinateClick[0]] + str(self.coordinateClick[1])
        move = str(self.clickfrom) + str(self.clickTo)

        #check promotion
        traceFrom = self.MAP[self.clickfrom[0]] + (self.NUMBER_ROW) * (int(self.clickfrom[1]) - 1)
        traceFrom = self.board.piece_at(traceFrom)
        if traceFrom.symbol() == 'p' and int(self.clickTo[1]) == 1:
            move += 'q'
        elif traceFrom.symbol() == 'P' and int(self.clickTo[1]) == 8:
            move += 'q'

        #print(move)
        move = chess.Move.from_uci(move)
        self.board.push(move)
        self.mapHightLight.clear()
        self.draw()
        self.slot[0] = False
        self.canvas.delete("move")
        self.canvas.create_text(20, 150, anchor='w', font="VNI-Dom 14",
                           text="White move: " + str(move), tag = "move")
        self.canvas.delete("status")
        self.canvas.create_text(20, 220, anchor='w', font="VNI-Dom 14",
                           text="Status board: Machine turn", tag = "status")

        self.game.ROOT.after(1000, self.game.AIplay)


    def draw(self):
        #delete canvas
        self.GUIBoard.delete("square")
        self.GUIBoard.delete("piece")
        collor = self.WHITE
        positonClick = None
        if len(self.coordinateClick):
            positonClick = self.coordinateClick[0] + (self.NUMBER_ROW)* (self.coordinateClick[1] - 1)
            #print(positonClick)
        for i in range(self.NUMBER_ROW):
            collor = self.BLACK if collor == self.WHITE else self.WHITE
            for j in range(self.NUMBER_COLLUM):
                pos = i * self.NUMBER_ROW + j
                if(collor == self.WHITE):
                    if positonClick is not None and positonClick == pos:
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                       self.square[pos][0] + self.SIZE_SQUARE,
                                                       self.square[pos][1] + self.SIZE_SQUARE, fill=self.GREEN, tag="square")
                    elif(pos in self.mapHightLight):
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                       self.square[pos][0] + self.SIZE_SQUARE,
                                                       self.square[pos][1] + self.SIZE_SQUARE, fill=self.YELLOW, tag="square")
                    else:
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                       self.square[pos][0] + self.SIZE_SQUARE,
                                                       self.square[pos][1] + self.SIZE_SQUARE, fill=self.WHITE, tag="square")
                    collor = self.BLACK
                else:
                    if positonClick is not None and positonClick == pos:
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                       self.square[pos][0] + self.SIZE_SQUARE,
                                                       self.square[pos][1] + self.SIZE_SQUARE, fill=self.GREEN, tag="square")
                    elif (pos in self.mapHightLight):
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                   self.square[pos][0] + self.SIZE_SQUARE,
                                                   self.square[pos][1] + self.SIZE_SQUARE, fill=self.YELLOW, tag="square")
                    else:
                        self.GUIBoard.create_rectangle(self.square[pos][0], self.square[pos][1],
                                                   self.square[pos][0] + self.SIZE_SQUARE,
                                                   self.square[pos][1] + self.SIZE_SQUARE, fill=self.BLACK, tag="square")
                    collor = self.WHITE

        offset = self.NUMBER_ROW*self.NUMBER_COLLUM
        for i in range(offset):
            pieceAtSquare = self.board.piece_at(i);
            if (pieceAtSquare is not None):
                image = pieceAtSquare.symbol()
                self.GUIBoard.create_image(self.SIZE_SQUARE // 2 + self.square[i][0],self.SIZE_SQUARE // 2 + self.square[i][1], image = self.piece[image], tag = "piece")
