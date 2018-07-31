import Config
from State import State
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from Move import Move
from AlphaBetaSearch import AlphaBetaSearch
import time,sys,os

class TicTacToe(App):
    """
    This is the main script for interactive Tic-Tac-Toe game
    """
    
    def build(self):
        """
        This method builds the GUI
        """
        #initialize
        self.currentState = State()
        self.winner = -1
        #array of buttons
        #so that we know which button is pressed and can change button text
        #when computer makes a move
        self.buttons = []
        #we need to change it later
        self.winnerLabel = None
        
        #create layout
        layout = FloatLayout(size=(300, 300))
        
        #find the width and height of the buttons
        colWidth = 0.75 / Config.nSquares
        rowHeight = 1.0 / Config.nSquares
        #create grid of buttons
        for i in range(Config.nSquares):
            for j in range(Config.nSquares):
                button = Button(text="-", size_hint=(colWidth, rowHeight),
                                pos_hint={'x':colWidth * i, 'y':rowHeight * j},
                                font_size=60)
                button.bind(on_press = self.selectBox)
                layout.add_widget(button) 
                #append buttons
                self.buttons.append(button) 
        #winner label
        self.winnerLabel = Label(text = "Winner is", size_hint=(.25, 1), 
                           pos_hint={'x':.75, 'y':0.},
                           font_size=20)
        layout.add_widget(self.winnerLabel) 
        
        #get first move in case of computer player goes first
        if Config.startPlayer == Config.computerPlayer:
            self.callComputerPlayer()
              
        return layout
    
    
    def callComputerPlayer(self):
        """
        This method calls the computer player's search algorithm 
        and makes the best move
        """
        search = AlphaBetaSearch(self.currentState,
                              Config.maximumDepth, False)
        bestMove = search.search()   
        if bestMove != None:
            #change button text
            self.buttons[bestMove.col * Config.nSquares + 2 - bestMove.row].text = \
                Config.moveTexts[Config.computerPlayer] 
            #change current state, board values
            self.currentState = self.currentState.createChildState(bestMove)
    
    
    def changeWinnerText(self):
        """
        This method finds the winning player
        and shows it in the GUI
        """
        if self.winner == Config.humanPlayer:
            self.winnerLabel.text = "Winner is Human"
        elif self.winner == Config.computerPlayer:
            self.winnerLabel.text = "Winner is Computer"
        elif self.winner == Config.drawValue:
            self.winnerLabel.text = "Game is draw"
        
        
    
    def selectBox(self, instance):
        """
        This sets the text of a button to human player's clicks
        instance is the button clicked
        """
        #if game has ended
        #we will not let the buttons to be clicked
        if self.winner != -1:
            return
        
        #check if that square the human clicked on is not occupied
        if instance.text == "-": 
            #change text of the button
            instance.text = Config.moveTexts[Config.humanPlayer]
            #mark it in the boardValues
            #find the row and column of the button
            for i in range(Config.nSquares):
                for j in range(Config.nSquares):
                    #fix the indexing issues
                    if self.buttons[j * Config.nSquares + 2 - i] == instance:
                        #create human move
                        humanMove = Move(i, j, Config.humanPlayer)
                        #update current state
                        self.currentState = self.currentState.createChildState(\
                                                humanMove)                
        
        #check if game has ended
        endFlag, self.winner = self.currentState.checkGoalState()
        if endFlag:
            print ("game has ended")
            print ("winner is", self.winner)
            self.changeWinnerText()
            return
            
        #call computer player
        self.callComputerPlayer()
            
        #check if game has ended
        endFlag, self.winner = self.currentState.checkGoalState()
        if endFlag:
            print ("game has ended")
            print ("winner is", self.winner)
            self.changeWinnerText()
                
TicTacToe().run()